from BACKEND_NAME_PLACEHOLDER.schema import EntityBase, EntityFull


def test_entity_00():
    entity_base = EntityBase(name="Ulmer")

    entity_base_copy: EntityBase = eval(
        repr(entity_base)
    )
    assert entity_base_copy.name == entity_base.name

    entity: EntityFull = EntityFull(id=1, name="Fritz")

    entity_copy: EntityFull = eval(repr(entity))

    assert entity_copy == entity

def test_fail():
    assert True
