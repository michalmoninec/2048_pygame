from simulations.monte_carlo import MonteCarlo


def get_attribute(obj: object, name: str):
    """Returns object attribute value if there is object attribute
    with provided name, otherwise returns None.
    """
    if obj is not None:
        return getattr(obj, name, None)
    return None


def test_init(mc_init_attrs: dict):
    """Tests initialization method of MonteCarlo class."""
    mc = MonteCarlo()

    for attr in mc_init_attrs["values"]:
        assert get_attribute(mc, attr) == mc_init_attrs["values"][attr]

    for attr in mc_init_attrs["types"]:
        assert type(get_attribute(mc, attr)) == mc_init_attrs["types"][attr]
