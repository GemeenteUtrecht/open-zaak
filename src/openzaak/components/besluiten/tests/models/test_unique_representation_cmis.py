# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2020 Dimpact
from django.test import override_settings, tag

from openzaak.components.documenten.tests.factories import (
    EnkelvoudigInformatieObjectFactory,
)
from openzaak.tests.utils import APICMISTestCase

from ...tests.factories import BesluitFactory, BesluitInformatieObjectFactory


@tag("cmis")
@override_settings(CMIS_ENABLED=True)
class UniqueRepresentationTestCMISCase(APICMISTestCase):
    def test_besluitinformatieobject(self):
        eio = EnkelvoudigInformatieObjectFactory.create(identificatie="12345")
        eio_url = eio.get_url()
        bio = BesluitInformatieObjectFactory(
            informatieobject=eio_url,
            besluit=BesluitFactory.create(
                **{"identificatie": "5d940d52-ff5e-4b18-a769-977af9130c04"}
            ),
        )

        self.assertEqual(
            bio.unique_representation(),
            "(5d940d52-ff5e-4b18-a769-977af9130c04) - 12345",
        )
