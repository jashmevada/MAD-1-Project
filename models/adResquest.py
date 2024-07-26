from flask import (Blueprint, render_template, session, redirect, url_for, request, jsonify, )
from flask_restful import Api, Resource, reqparse
from time import time
from marshmallow import Schema, fields
from pprint import pprint

from models.model import *

bp = Blueprint('ad_request', __name__, url_prefix='/ad_request')

# Api -------------------------------

api = Api(bp)
parser = reqparse.RequestParser()
parser.add_argument('budget', type=str, location='args')
parser.add_argument('message', type=str)
parser.add_argument('camp', type=str)
parser.add_argument('status', type=str)


class InfluencerInfoSchema(Schema):
    sponsor_names = fields.List(fields.Str())
    campaign_title = fields.List(fields.Str())
    message = fields.List(fields.Str())
    description = fields.List(fields.Str())
    budget_of_campaign = fields.List(fields.Int())
    budget_from_sponsor = fields.List(fields.Int())


class AdRequestSponsorAPI(Resource):
    def get(self, username):
        return {"je;;": username}

    def put(self):
        pass

    def post(self, username):
        print(username)
        args = parser.parse_args()
        print(args)
        # print(request.form)
        print(request.args)

        data = AdRequest(
            campaign_id=args['camp'],
            influencer_id=request.args['influ_id'],
            message=args['message'],
            payment_amount=args['budget'],
            status=args['status'],
            sponsor_id=session['username']
        )

        db.session.add(data)
        db.session.commit()
        return {"status": "success"}, 201

    def delete(self):
        pass


schema = InfluencerInfoSchema()


class AdRequestInfluencerAPI(Resource):

    def get(self, username):
        # Response type : { sponsor name, campaign title, message, description of campaign ,budget, dates }
        t1 = time()
        req = get_ad_for_influencer(username)
        # sponsor_name = [Sponsor.query.filter_by(user_id=i.sponsor_id).all() for i in req]
        camps = [[j for j in Campaign.query.filter_by(id=i.campaign_id).all()] for i in req]
        # print(camps)
        send_data = {
            'sponsor_names': [Sponsor.query.get(req[i].sponsor_id).full_name for i in range(len(req))],
            # [[j.full_name for j in i] for i in sponsor_name],
            'campaign_title': [req[i].campaign.title for i in range(len(req))],
            # [[j.title for j in camp] for camp in camps],
            'message': [i.message for i in req],
            'description': [req[i].campaign.description for i in range(len(req))],
            # [[j.description for j in camp] for camp in camps] ,# [[j.description for j in Campaign.query.filter_by(id=i.campaign_id).all()] for i in req],
            'budget_of_campaign': [req[i].campaign.budget for i in range(len(req))],
            # [[j.budget for j in camp] for camp in camps] ,#[[j.budget for j in Campaign.query.filter_by(id=i.campaign_id).all()] for i in req],
            'budget_from_sponsor': [i.payment_amount for i in req],
        }
        t2 = time()
        print(t2 - t1)

        pprint(schema.dump(send_data))
        # print(req[1].campaign.title)
        return schema.dump(send_data)

    def put(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass


api.add_resource(AdRequestSponsorAPI, '/api/sponsor/<username>', '/api/sponsor/')
api.add_resource(AdRequestInfluencerAPI, '/api/influencer/<username>', '/api/influencer/')


# Utils Functions -----------------------

def get_current_requests() -> list[AdRequest]:
    lst = []
    for i in Campaign.query.filter(Campaign.sponsor_id == Sponsor.query.get(session['username']).user_id).all():
        lst.append(i)

    return [AdRequest.query.filter_by(campaign_id=i.id).all() for i in lst]


def get_ad_for_influencer(username) -> list[AdRequest]:
    return AdRequest.query.filter_by(influencer_id=username).all()


# Routes --------------------------------

@bp.route('/create', methods=['POST'])
def create_ad_request():
    return render_template("sponsor/find_inf.html", active_tab="find", infs=Influencer.query.all(),
                           cmps=Campaign.query.filter(
                               Campaign.sponsor_id == Sponsor.query.get(session['username']).user_id).all(), )


@bp.route('/')
def index():
    all_reqs = get_current_requests()
    return render_template("sponsor/send_request.html", active_tab="adrequest", reqs=all_reqs)


@bp.route('/influ_req')
def influ_req():
    return render_template("influencer/ad_request.html", active_tab="adrequest", reqs=get_current_requests())
