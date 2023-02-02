# -*- coding: utf-8 -*-
"""
    :author: Grey Li (李辉)
    :url: http://greyli.com
    :copyright: © 2018 Grey Li <withlihui@gmail.com>
    :license: MIT, see LICENSE for more details.
"""
from flask import render_template, request, Blueprint, jsonify
from flask_login import current_user, login_required
from betterReadingRecord.extensions import db
from betterReadingRecord.models import ReadRecord,Book
from datetime import datetime

read_record_bp = Blueprint('read_record', __name__)


@read_record_bp.route('/read-record',methods=['GET', 'POST', 'DELETE', 'PUT'])
@login_required
def app():
    if request.method == 'GET':
        all_count = ReadRecord.query.with_parent(current_user).count()
        list = []
        for record in current_user.read_records:
            list.append(record.as_dict())
        return {
            'list':list,
            'all_count':all_count,
        }

    if request.method == 'POST':
        data = request.get_json()
        date = datetime.strptime(data['date'],'%Y-%m-%d')
        book_name = data['book_name']
        start_time = datetime.strptime(data['start_time'],'%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(data['end_time'],'%Y-%m-%d %H:%M:%S')

        book = Book.query.filter_by(book_name=book_name).first()
        if not book:
            new_book = Book(book_name=book_name)
            db.session.add_all([new_book])
            db.session.commit()
            book = new_book

        record = ReadRecord(date=date,book_name=book.book_name
        ,start_time=start_time,end_time=end_time, user=current_user._get_current_object()
        )
        db.session.add_all([record])
        db.session.commit()

        return jsonify(message='add success.'), 200

    if request.method == 'DELETE':
        data = request.get_json()
        record_id = data['id']
        record = ReadRecord.query.get_or_404(record_id)
        if current_user != record.user:
            return jsonify(message='Permission denied.'), 403
        db.session.delete(record)
        db.session.commit()
        return jsonify(message='Record deleted.')        

    if request.method == 'PUT':
        data = request.get_json()
        record_id = data['id']
        record = ReadRecord.query.get_or_404(record_id)
        if current_user != record.user:
            return jsonify(message='Permission denied.'), 403

        date = datetime.strptime(data['date'],'%Y-%m-%d')
        book_name = data['book_name']
        start_time = datetime.strptime(data['start_time'],'%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(data['end_time'],'%Y-%m-%d %H:%M:%S')   

        record.date = date
        record.book_name = book_name
        record.start_time = start_time
        record.end_time = end_time        
        db.session.commit()
        return jsonify(message='Record updated.')