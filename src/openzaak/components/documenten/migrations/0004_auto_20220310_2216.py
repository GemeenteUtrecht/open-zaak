# SPDX-License-Identifier: EUPL-1.2
# Copyright (C) 2022 Dimpact
# Generated by Django 3.2.12 on 2022-03-10 22:16

from django.db import migrations

import django_loose_fk.constraints


class Migration(migrations.Migration):

    dependencies = [
        ("documenten", "0003_auto_20200124_1021"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="enkelvoudiginformatieobject",
            name="_informatieobjecttype_or__informatieobjecttype_url_filled",
        ),
        migrations.AddConstraint(
            model_name="enkelvoudiginformatieobject",
            constraint=django_loose_fk.constraints.FkOrURLFieldConstraint(
                app_label="documenten",
                fk_field="_informatieobjecttype",
                model_name="enkelvoudiginformatieobject",
                url_field="_informatieobjecttype_url",
            ),
        ),
    ]