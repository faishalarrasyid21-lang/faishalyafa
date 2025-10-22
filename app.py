from flask import Flask, render_template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'netflix_titles.csv')


def load_data(path=DATA_PATH):
    df = pd.read_csv(path)
    # Basic cleaning following the notebook
    cols_to_fill = ['director', 'cast', 'country', 'date_added']
    for c in cols_to_fill:
        if c in df.columns:
            df[c] = df[c].fillna('Unknown')

    if 'date_added' in df.columns:
        df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
        df['year_added'] = df['date_added'].dt.year.fillna(0).astype(int)
    else:
        df['year_added'] = 0

    from flask import Flask, render_template
    import pandas as pd
    import numpy as np
    import plotly.express as px
    import plotly.io as pio
    import os

    app = Flask(__name__, template_folder='templates', static_folder='static')

    # The CSV is expected to live in the same folder as this file (netflix_flask_app)
    DATA_PATH = os.path.join(os.path.dirname(__file__), 'netflix_titles.csv')


    def load_data(path=DATA_PATH):
        df = pd.read_csv(path)
        # Basic cleaning following the notebook
        cols_to_fill = ['director', 'cast', 'country', 'date_added']
        for c in cols_to_fill:
            if c in df.columns:
                df[c] = df[c].fillna('Unknown')

        if 'date_added' in df.columns:
            df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
            df['year_added'] = df['date_added'].dt.year.fillna(0).astype(int)
        else:
            df['year_added'] = 0

        # duration
        if 'duration' in df.columns:
            df = df.dropna(subset=['duration'])
            df['duration_num'] = df['duration'].str.extract('(\d+)').astype(float)
            df['duration_min'] = np.where(df.get('type') == 'Movie', df['duration_num'], np.nan)
            df['num_seasons'] = np.where(df.get('type') == 'TV Show', df['duration_num'], np.nan)

        # unnest listed_in (genre) and country
        if 'listed_in' in df.columns:
            genre_df = df.assign(listed_in=df['listed_in'].str.split(', ')).explode('listed_in')
        else:
            genre_df = df.copy()

        if 'country' in df.columns:
            country_df = df.assign(country=df['country'].str.split(', ')).explode('country')
        else:
            country_df = df.copy()

        return df, genre_df, country_df


    def make_figures(df, genre_df, country_df):
        figs = []

        # Fig 1: Pie chart content type
        if 'type' in df.columns:
            type_counts = df['type'].value_counts().reset_index()
            type_counts.columns = ['Content Type', 'Count']
            fig1 = px.pie(type_counts, names='Content Type', values='Count',
                          title='1. Proporsi Konten Netflix (Film vs. Acara TV)',
                          color_discrete_sequence=px.colors.qualitative.Set1)
            # include plotlyjs once (we load CDN in template), so include for first fig only
            figs.append(pio.to_html(fig1, full_html=False, include_plotlyjs='cdn'))

        # Fig 2: Trend per year
        if 'year_added' in df.columns:
            df_yearly = df[df['year_added'] >= 2008].groupby('year_added')['show_id'].count().reset_index(name='Total Content Added')
            fig2 = px.line(df_yearly, x='year_added', y='Total Content Added',
                           title='2. Tren Jumlah Konten Baru Ditambahkan per Tahun',
                           markers=True, line_shape='spline')
            fig2.update_layout(xaxis_title='Tahun Ditambahkan', yaxis_title='Jumlah Konten')
            figs.append(pio.to_html(fig2, full_html=False, include_plotlyjs=False))

        # Fig 3: Top countries
        if 'country' in country_df.columns:
            top_countries = country_df[country_df['country'] != 'Unknown']['country'].value_counts().head(10).reset_index()
            top_countries.columns = ['Country', 'Count']
            fig3 = px.bar(top_countries, x='Count', y='Country', orientation='h',
                          title='3. Top 10 Negara Kontributor Konten Terbanyak',
                          color='Count', color_continuous_scale=px.colors.sequential.Plasma)
            fig3.update_layout(yaxis={'categoryorder':'total ascending'})
            figs.append(pio.to_html(fig3, full_html=False, include_plotlyjs=False))

        # Fig 4: Top genres
        if 'listed_in' in genre_df.columns:
            top_genres = genre_df['listed_in'].value_counts().head(10).reset_index()
            top_genres.columns = ['Genre', 'Count']
            fig4 = px.bar(top_genres, x='Count', y='Genre', orientation='h',
                          title='4. Top 10 Genre Paling Populer',
                          color='Count', color_continuous_scale=px.colors.sequential.Viridis)
            fig4.update_layout(yaxis={'categoryorder':'total ascending'})
            figs.append(pio.to_html(fig4, full_html=False, include_plotlyjs=False))

        # Fig 5: Duration histogram
        if 'duration_min' in df.columns:
            df_movies = df.dropna(subset=['duration_min'])
            fig5 = px.histogram(df_movies, x='duration_min',
                                title='5. Distribusi Durasi Film (dalam Menit)',
                                nbins=30, marginal='box')
            fig5.update_layout(xaxis_title='Durasi Film (Menit)')
            figs.append(pio.to_html(fig5, full_html=False, include_plotlyjs=False))

        # Fig 6: Rating distribution
        if 'rating' in df.columns:
            rating_counts = df['rating'].value_counts().reset_index()
            rating_counts.columns = ['Rating', 'Count']
            fig6 = px.bar(rating_counts, x='Rating', y='Count',
                          title='6. Distribusi Klasifikasi Rating Usia',
                          color='Count', color_continuous_scale=px.colors.sequential.Agsunset)
            figs.append(pio.to_html(fig6, full_html=False, include_plotlyjs=False))

        return figs


    @app.route('/')
    def index():
        df, genre_df, country_df = load_data()
        graphs = make_figures(df, genre_df, country_df)
        return render_template('index.html', graphs=graphs)


    if __name__ == '__main__':
        # Simple local runner for development (not used by PythonAnywhere WSGI)
        app.run(debug=True, host='0.0.0.0')
