from flask import url_for

articles = [
        {
            "id": "1",
            "title": "Bedoes jest wpisany na liste *zobacz jak*",
            "description": "Nie kłócił się bo ochroniarz był duży, okazało sie że jest na liście",
            "header_image_url": url_for("static", filename="img/bedinaliscie.jpg"),
            "content": "Płyta \"RODZINNY BIZNES\", out now"
        },
        {
            "id": "2"
        },
        {
            "id": "3"
        }
    ]