# -*- coding: utf-8 -*-

from numpy import datetime64


from openfisca_tunisia.model.base import *


class idmen(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # 600001, 600002,


class idfoy(Variable):
    column = IntCol(is_permanent = True)
    entity_class = Individus
    # idmen + noi du déclarant


class quimen(Variable):
    column = EnumCol(QUIMEN, is_permanent = True)
    entity_class = Individus


class quifoy(Variable):
    column = EnumCol(QUIFOY, is_permanent = True)
    entity_class = Individus


class age(Variable):
    column = AgeCol(val_type = "age")
    entity_class = Individus
    label = u"Âge (en années)"

    def function(self, simulation, period):
        date_naissance = simulation.get_array('date_naissance', period)
        if date_naissance is None:
            age_en_mois = simulation.get_array('age_en_mois', period)
            if age_en_mois is not None:
                return period, age_en_mois // 12
            date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.date) - date_naissance).astype('timedelta64[Y]')


class age_en_mois(Variable):
    column = AgeCol(val_type = "months")
    entity_class = Individus
    label = u"Âge (en mois)"

    def function(self, simulation, period):
        date_naissance = simulation.get_array('date_naissance', period)
        if date_naissance is None:
            age = simulation.get_array('age', period)
            if age is not None:
                return period, age * 12
            date_naissance = simulation.calculate('date_naissance', period)
        return period, (datetime64(period.date) - date_naissance).astype('timedelta64[M]')


class date_naissance(Variable):
    column = DateCol(is_permanent = True)
    entity_class = Individus
    label = u"Année de naissance"


class male(Variable):
    column = BoolCol()
    entity_class = Individus
    label = u"Mâle"


class marie(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Marié(e)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)

        return period, (statut_marital == 1)


class celibataire(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Célibataire"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)

        return period, (statut_marital == 2)


class divorce(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Divorcé(e)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)
        return period, (statut_marital == 3)


class veuf(Variable):
    column = BoolCol
    entity_class = Individus
    label = u"Veuf(ve)"

    def function(self, simulation, period):
        period = period.start.offset('first-of', 'month').period('year')
        statut_marital = simulation.calculate('statut_marital', period = period)
        return period, statut_marital == 4


class statut_marital(Variable):
    column = PeriodSizeIndependentIntCol(default = 2)
    entity_class = Individus
