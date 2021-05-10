import dash_bootstrap_components as dbc


def Navbar():
    navbar = dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/index")),
            dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Page 2", href="#"),
                    dbc.DropdownMenuItem("Page 3", href="#"),
                ],
                nav=True,
                in_navbar=True,
                label="More",
            ),
        ],
        brand="Indicadores de Recursos Humanos do Comando-Geral de Apoio (COMGAP)",
        color="primary",
        dark=True,
    )
    return navbar
