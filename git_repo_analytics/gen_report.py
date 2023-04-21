import os

import duckdb
import matplotlib.pyplot as plt
import pandas as pd
import webbrowser


def generate_table():
    with duckdb.connect(database='data/git_repo.duckdb') as conn:
        css = [{'selector': 'th',
                'props': [('background-color', 'lightgrey'),
                          ('color', 'black'),
                          ('font-weight', 'bold'),
                          ('padding', '5px')]},
               {'selector': 'td',
                'props': [('padding', '5px')]}]

        df = conn.query('SELECT * FROM repos').fetchdf()
        df = df.fillna('')
        df = df.replace({pd.NaT: None})
        styled_table = df.style.set_table_styles(css)

        styled_table = styled_table.format({'repo': lambda url: f'<a href="https://github.com/{url}">{url}</a>',
                                            'homepage': lambda url: f'<a href="{url}">{url}</a>'})
        html_table = styled_table.to_html(index=False)
    return html_table


def generate_chart(path):
    with duckdb.connect(database='data/git_repo.duckdb') as conn:
        df = conn.query('SELECT * FROM commit_weekly').fetchdf()
        fig, ax = plt.subplots()

        for key, grp in df.groupby('repo'):
            ax = grp.plot(ax=ax, kind='line', x='date_week', y='total_commits', label=key)
        plt.legend(loc='best')
        plt.savefig(path)


def generate():
    html_table = generate_table()
    os.makedirs('data/report', exist_ok=True)
    generate_chart('data/report/weekly_commits.png')
    html_path = 'data/report/index.html'
    with open(html_path, 'w') as f:
        f.write('<html><body>')
        f.write('<h2>Git repo analytics</h2>')
        f.write(html_table)
        f.write('<h3>Weekly commits</h3>')
        f.write("<img src='weekly_commits.png'>")
        f.write('</body></html>')

    abs_html_path = os.path.abspath(html_path)
    print(f"Report generated at {abs_html_path}")
    webbrowser.open('file://' + abs_html_path)


if __name__ == '__main__':
    generate()
