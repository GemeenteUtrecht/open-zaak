# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2020 Dimpact
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.test import TestCase

from notifications_api_common.constants import (
    SCOPE_NOTIFICATIES_CONSUMEREN_LABEL,
    SCOPE_NOTIFICATIES_PUBLICEREN_LABEL,
)
from notifications_api_common.models import NotificationsConfig
from vng_api_common.authorizations.models import Applicatie, Autorisatie
from vng_api_common.constants import ComponentTypes
from vng_api_common.models import APICredential, JWTSecret
from zgw_consumers.constants import APITypes, AuthTypes
from zgw_consumers.models import Service

from openzaak.components.autorisaties.api.scopes import SCOPE_AUTORISATIES_LEZEN
from openzaak.notifications.tests.mixins import NotificationsConfigMixin


class SetupConfigurationTests(NotificationsConfigMixin, TestCase):
    def test_setup_configuration(self):
        openzaak_domain = "open-zaak.utrecht.nl"
        nrc_root = "https://open-notificaties.utrecht.nl/api/v1/"
        municipality = "Utrecht"
        openzaak_to_notif_secret = "12345"
        notif_to_openzaak_secret = "54321"

        call_command(
            "setup_configuration",
            openzaak_domain,
            nrc_root,
            municipality,
            openzaak_to_notif_secret,
            notif_to_openzaak_secret,
        )

        site = Site.objects.get_current()
        self.assertEqual(site.domain, openzaak_domain)
        self.assertEqual(site.name, f"Open Zaak {municipality}")

        service = Service.objects.get(api_type=APITypes.nrc)
        self.assertEqual(service.api_root, nrc_root)
        self.assertEqual(service.auth_type, AuthTypes.zgw)
        self.assertEqual(service.user_id, "open-zaak")
        self.assertEqual(service.user_representation, "Open Zaak")

        notif_config = NotificationsConfig.get_solo()
        self.assertEqual(notif_config.notifications_api_service, service)

        api_credential = APICredential.objects.get()
        self.assertEqual(api_credential.api_root, nrc_root)
        self.assertEqual(
            api_credential.label, f"Open Notificaties {municipality}",
        )
        self.assertEqual(api_credential.client_id, f"open-zaak-{municipality.lower()}")
        self.assertEqual(api_credential.secret, openzaak_to_notif_secret)
        self.assertEqual(api_credential.user_id, f"open-zaak-{municipality.lower()}")
        self.assertEqual(
            api_credential.user_representation, f"Open Zaak {municipality}"
        )

        notif_api_jwtsecret_ac = JWTSecret.objects.get()
        self.assertEqual(
            notif_api_jwtsecret_ac.identifier,
            f"open-notificaties-{municipality.lower()}",
        )
        self.assertEqual(notif_api_jwtsecret_ac.secret, notif_to_openzaak_secret)

        notif_api_applicatie_ac = Applicatie.objects.get(
            label=f"Open Notificaties {municipality}"
        )
        self.assertEqual(
            notif_api_applicatie_ac.client_ids, [notif_api_jwtsecret_ac.identifier]
        )

        notif_api_autorisatie_ac = Autorisatie.objects.get(
            applicatie=notif_api_applicatie_ac
        )
        self.assertEqual(notif_api_autorisatie_ac.component, ComponentTypes.ac)
        self.assertEqual(
            notif_api_autorisatie_ac.scopes, [SCOPE_AUTORISATIES_LEZEN.label]
        )

        openzaak_applicatie_notif = Applicatie.objects.get(
            label=f"Open Zaak {municipality}"
        )
        self.assertEqual(
            openzaak_applicatie_notif.client_ids, [f"open-zaak-{municipality.lower()}"]
        )

        openzaak_autorisatie_notif = Autorisatie.objects.get(
            applicatie=openzaak_applicatie_notif
        )
        self.assertEqual(openzaak_autorisatie_notif.component, ComponentTypes.nrc)
        self.assertEqual(
            openzaak_autorisatie_notif.scopes,
            [SCOPE_NOTIFICATIES_CONSUMEREN_LABEL, SCOPE_NOTIFICATIES_PUBLICEREN_LABEL,],
        )
