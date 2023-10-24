from typing import Type, Union

import pydantic
from flask import Flask, jsonify, request
from flask.views import MethodView

from models import Session, Advertisement
from schema import CreateAdvertisement, UpdateAdvertisement

firstapp = Flask("server_app")


class HttpError(Exception):
    """ Создаёт собственный класс исключений """
    def __init__(self, status_code: int, message: Union[str, dict, list]):
        self.status_code = status_code
        self.message = message


# @app.errorhandler(HttpError)
def error_handler(er: HttpError):
    """ Перехватывает исключения класса HttpError, отправляет сообщение об ошибке клиенту
        и прерывает выполнение программы. Вызывается при возникновении исключения HttpError.
    """
    response = jsonify({"status": "error", "message": er.message})
    response.status_code = er.status_code
    return response


def validate(validation_schema: Union[Type[CreateAdvertisement], Type[UpdateAdvertisement]], json_data):
    try:
        pydantic_obj = validation_schema(**json_data)
        return pydantic_obj.model_dump(exclude_none=True)
    except pydantic.ValidationError as er:
        raise HttpError(400, er.errors())


def get_advert(session: Session, advert_id: int):
    advert = session.get(Advertisement, advert_id)
    if advert is None:
        raise HttpError(404, f"Advertisement '{advert_id}' not found")
    return advert


class AdvertisementViews(MethodView):

    def get(self, advert_id: int):
        with Session() as session:
            advert = get_advert(session, advert_id)
            return jsonify({
                "id": advert_id,
                "description": advert.description,
                "creation_time": advert.creation_time.isoformat(),    # Преобразует дату в строчку, для JSON.
                "owner": advert.owner}
            )

    def post(self):
        validated_data = validate(CreateAdvertisement, request.json)
        with Session() as session:
            new_advert = Advertisement(**validated_data)
            session.add(new_advert)
            session.commit()
        return jsonify({"id": new_advert.id, "title": new_advert.title,
                        "creation_time": new_advert.creation_time.isoformat(), "owner": new_advert.owner})

    def patch(self, advert_id: int):
        validated_data = validate(UpdateAdvertisement, request.json)
        with Session() as session:
            advert = get_advert(session, advert_id)
            for field, value in validated_data.items():
                setattr(advert, field, value)
            session.add(advert)
            session.commit()
        return jsonify({"id": advert.id, "title": advert.title,
                        "creation_time": advert.creation_time.isoformat(), "owner": advert.owner})

    def delete(self, advert_id: int):
        with Session() as session:
            advert = get_advert(session, advert_id)
            session.delete(advert)
            session.commit()
        return jsonify({f"Status '{advert_id}':": "Delete"})


advert_view = AdvertisementViews.as_view(name="adverts")

firstapp.add_url_rule(rule="/advert/<int:advert_id>", view_func=advert_view, methods=["GET", "PATCH", "DELETE"])

firstapp.add_url_rule(rule="/advert", view_func=advert_view, methods=["POST"])

if __name__ == "__main__":
    firstapp.run()
