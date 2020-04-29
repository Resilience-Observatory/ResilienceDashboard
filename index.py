import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import app
from apps import app_credits, app1

#APP INDEX STRING
app.index_string = '''
<!DOCTYPE html>
<html class = "">

    <head>
        {%metas%}
        <title>RESILIENCE OBSERVATORY</title>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.8.0/css/bulma.min.css">
        <script defer src="https://use.fontawesome.com/releases/v5.3.1/js/all.js"></script>
        <link href='https://fonts.googleapis.com/css?family=Megrim' rel='stylesheet'>
            <style>
                .logo1 {
                    color : white;
                    font-family: 'Megrim';
                    font-size: 30px;
                }
                .navlogo {
                    background: linear-gradient(to left, #009999, #006666);
                }
            </style>
        {%favicon%}
        {%css%}
    </head>

    <body class="body">

        <nav class="navbar navlogo" role="navigation" aria-label="main navigation">

          <div class="navbar-brand">
            <a class="navbar-item logo1" href="/">RESILIENCE OBSERVATORY</a>
            <div class="navbar-burger burger" data-target="navMenu">
              <span></span>
              <span></span>
              <span></span>
            </div>
          </div>

          <div id="navMenu" class="navbar-menu">

            <div class="navbar-start">
              <a class="navbar-item" href="/apps/app1">DASHBOARD</a>
              <a class="navbar-item" href="/credits">INFO</a>
            </div>

          </div>
        </nav>

        <script type="text/javascript">
            document.addEventListener('DOMContentLoaded', () => {

            // Get all "navbar-burger" elements
            const $navbarBurgers = Array.prototype.slice.call(document.querySelectorAll('.navbar-burger'), 0);

            // Check if there are any navbar burgers
            if ($navbarBurgers.length > 0) {

                // Add a click event on each of them
                $navbarBurgers.forEach( el => {
                    el.addEventListener('click', () => {

                        // Get the target from the "data-target" attribute
                        const target = el.dataset.target;
                        const $target = document.getElementById(target);

                        // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
                        el.classList.toggle('is-active');
                        $target.classList.toggle('is-active');

                    });
                });
            }

            });
        </script>

        <section class="hero"
            {%app_entry%}
        </section>

        <footer class="footer hero has-text-centered">
                <a class='subtitle is-4 is-primary' href="https://ultrahack.org/covid-19datahack/data-against-covid-19" target='_blank'>Data Against COVID-19</a>
                <a class='subtitle is-4 is-primary' href="https://github.com/Resilience-Observatory" target='_blank'>Source code in GitHub</a>
                {%config%}
                {%scripts%}
                {%renderer%}
        </footer>

    </body>

</html>
'''

#APP LAYOUT DIV
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

#CHANGE PAGE DEPENDING ON PATHNAME
@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return app1.layout
    elif pathname == '/apps/app1':
         return app1.layout
    else:
        return app_credits.layout

#START THE SERVER
if __name__ == '__main__':
    app.run_server(port=80, host='0.0.0.0', debug=True)
