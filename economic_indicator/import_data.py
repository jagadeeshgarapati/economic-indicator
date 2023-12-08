import requests
from economic_indicator.database import connect_db


def fetch_data(country_code, indicator):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data[1] if data[0]['total'] > 0 else None
    else:
        return None


def insert_data(data, country, indicator):
    conn = connect_db()
    cursor = conn.cursor()

    for record in data:
        year = record['date']
        value = record.get('value')
        if value is not None:
            cursor.execute(f"INSERT INTO economic_indicators (country_code, year, {indicator}) VALUES (%s, %s, %s) ON CONFLICT (country_code, year) DO UPDATE SET {indicator} = EXCLUDED.{indicator};", (country, year, value))

    conn.commit()
    cursor.close()
    conn.close()


def import_data():
    countries = ['CN', 'IN', 'VN', 'ID', 'SG', 'KR', 'MY']
    indicators = {
        'gdp_growth_rate': 'NY.GDP.MKTP.KD.ZG',
        'population_growth_rate': 'SP.POP.GROW',
        'gni_per_capita': 'NY.GNP.PCAP.CD',
        'inflation_rate': 'FP.CPI.TOTL.ZG',
        'government_debt': 'GC.DOD.TOTL.GD.ZS',
        'fdi_net_inflows': 'BX.KLT.DINV.WD.GD.ZS',
        'ease_of_doing_business': 'IC.BUS.EASE.XQ',
        'export_percent_gdp': 'NE.EXP.GNFS.ZS',
        'import_percent_gdp': 'NE.IMP.GNFS.ZS'
    }

    for country in countries:
        for indicator_name, indicator_code in indicators.items():
            print(f"Fetching data for {country}, indicator: {indicator_name}")
            data = fetch_data(country, indicator_code)
            if data:
                print(f"Inserting data for {country}, indicator: {indicator_name}")
                insert_data(data, country, indicator_name)


if __name__ == '__main__':
    import_data()
