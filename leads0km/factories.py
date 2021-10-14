import cuid

import factory
import factory.fuzzy

from leads0km import leads0km


class FlatLeadFactory(factory.Factory):
    campania = factory.fuzzy.FuzzyText()
    source = factory.fuzzy.FuzzyText()
    nombre = factory.fuzzy.FuzzyText()
    telefono = factory.fuzzy.FuzzyText()
    email = factory.fuzzy.FuzzyText()
    provincia = factory.fuzzy.FuzzyText()
    mensaje = factory.fuzzy.FuzzyText()
    marca = factory.fuzzy.FuzzyText()
    modelo = factory.fuzzy.FuzzyText()
    vendedor = factory.fuzzy.FuzzyText()
    valor1 = factory.fuzzy.FuzzyText()
    valor2 = factory.fuzzy.FuzzyText()

    class Meta:
        model = leads0km.FlatLead


class LeadFactory(factory.Factory):
    campania = factory.fuzzy.FuzzyText()
    source = factory.fuzzy.FuzzyText()
    nombre = factory.fuzzy.FuzzyText()
    telefono = factory.fuzzy.FuzzyText()
    email = factory.fuzzy.FuzzyText()
    provincia = factory.fuzzy.FuzzyText()
    mensaje = factory.fuzzy.FuzzyText()
    marca = factory.fuzzy.FuzzyText()
    modelo = factory.fuzzy.FuzzyText()
    vendedor = factory.fuzzy.FuzzyText()
    extra = factory.LazyAttribute(lambda obj: {cuid.cuid(): cuid.cuid(),
        cuid.cuid(): cuid.cuid()})

    class Meta:
        model = leads0km.Lead
