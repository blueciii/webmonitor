import utils


def test_invalid_site():
    site = 'feadasf.fasdf.com.au'
    (response, err), duration = utils.check_website(site)

    assert response is None
    assert type(duration) == float


def test_valid_site():
    site = 'https://aiven.io'
    (response, err), duration = utils.check_website(site)
    
    assert response.status_code == 200
    assert type(duration) == float


def test_check_site():
    sites_data = [
        {
            "url": "https://google.com",
            "pattern": "^<!doctype[ a-zA-Z<>:\\/.\\=\\-\"]+<head>"
        },
        {
            "url": "https://aiven.io",
            "pattern": "<h1 color=\"[a-z]+\" class=\"[a-z0-9A-Z -]+\">Performant data pipelines in minutes<\\/h1>"
        },
        {
            "url": "https://www.python.org/"
        },
        {
            "pattern": "fsafsdgsdgasd"
        }
    ]

    status_list = utils.check_sites(sites_data)
    print(status_list)
    assert len(status_list) == 3
    assert all(key in status_list[0] for key in ['site', 'httpcode', 'duration', 'pattern','error', 'history'])
