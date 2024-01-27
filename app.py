from flask import Flask,render_template,request,session,redirect 
from flask_sqlalchemy import SQLAlchemy
import json #config.json

#config.json
with open('config.json','r') as c:
    params=json.load(c) ["params"]

app = Flask(__name__)

#db-connectivity
local_server=True
if(local_server):
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

db=SQLAlchemy(app)


#db-table
class Courses(db.Model):
    course_id= db.Column(db.Integer, primary_key=True)
    course_name= db.Column(db.String(50),nullable=False)
    course_code= db.Column(db.String(10),nullable=False)
    duration= db.Column(db.String(10),nullable=False)
   

class Students(db.Model):
    student_id= db.Column(db.Integer, primary_key=True)
    student_name= db.Column(db.String(50),nullable=False)
    prn= db.Column(db.String(20),nullable=False)
    sem= db.Column(db.String(2),nullable=False)
    
    
class Allocation(db.Model):
    allocation_id= db.Column(db.Integer, primary_key=True)
    student_id= db.Column(db.String(50),nullable=False)
    course_id= db.Column(db.String(30),nullable=False)


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/courses",methods=['GET','POST'])
def courses():

    if(request.method=='POST'):
        name=request.form.get('cname')
        code=request.form.get('ccode')
        duration=request.form.get('cduration')
        
        entry=Courses(course_name=name, course_code=code, duration=duration)
        db.session.add(entry)
        db.session.commit()

    c=Courses.query.all()
    return render_template('courses.html',params=params,course=c)
    

@app.route("/students",methods=['GET','POST'])
def students():
    if(request.method=='POST'):
        student_name=request.form.get('name')
        sem=request.form.get('sem')
        prn=request.form.get('prn')
        
        entry=Students(student_name=student_name, sem=sem, prn=prn)
        db.session.add(entry)
        db.session.commit()

    s=Students.query.all()
    return render_template('students.html',params=params,student=s)

@app.route("/course_add")
def course_add(): 
    return render_template('courses_add.html',params=params)

@app.route("/student_add")
def student_add(): 
    course=Courses.query.all()
    return render_template('student_add.html',params=params, course=course)


@app.route("/student_edit/<string:sno>" ,methods=['GET','POST'])
def student_edit(sno): 
    if request.method=='POST':
            name1=request.form.get('name')
            sem1=request.form.get('sem')
            prn1=request.form.get('prn')
           

            post=Students.query.filter_by(student_id=sno).first()
            post.student_name=name1
            post.sem=sem1
            post.prn=prn1
            db.session.commit()
        
            s=Students.query.all()
            return render_template('students.html',params=params,student=s)
    
    post=Students.query.filter_by(student_id=sno).first()
    return render_template('student_edit.html',params=params,post=post)


@app.route("/student_delete/<string:sno>",methods=['GET'])
def delete(sno):
    
        post=Students.query.filter_by(student_id=sno).first()
        db.session.delete(post)
        db.session.commit()
        s=Students.query.all()
        return render_template('students.html',params=params,student=s)

@app.route("/course_delete/<string:sno>",methods=['GET'])
def course_delete(sno):
        
        posts=Courses.query.filter_by(course_id=sno).first()
        
        db.session.delete(post)
        db.session.commit()
        
        c=Courses.query.all()
        return render_template('courses.html',params=params,course=c)



@app.route("/allot_course/<string:sno>",methods=['GET','POST'])
def allot_course(sno):
        

        c=Courses.query.all()
        post=Students.query.filter_by(student_id=sno).first()
        reg_courses=Allocation.query.filter_by(student_id=sno).all()
        # course = Courses.query.get(course_id)
        course = [Courses.query.get(allocation.course_id) for allocation in reg_courses]
        
        return render_template('allot_course.html',params=params,students=post, course=course, c=c)



@app.route("/allot_course_add",methods=['GET','POST'])
def allot_course_add():

    if(request.method=='POST'):
        cid=request.form.get('selected_course')
        sid=request.form.get('sid')
        
        
        entry=Allocation(course_id=cid, student_id=sid, )
        db.session.add(entry)
        db.session.commit()

        
    return redirect('/allot_course/'+sid)

    # s=Students.query.all()
    # return render_template('students.html',params=params,student=s)

@app.route("/allocation_delete/<string:sno>/<string:cno>",methods=['GET'])
def allocation_delete(sno,cno):
    
        posts = Allocation.query.filter_by(student_id=sno, course_id=cno).all()

        if posts:
            for post in posts:
                db.session.delete(post)
            db.session.commit()
        return redirect('/allot_course/'+sno)

@app.route("/students_registered/<string:cno>",methods=['GET'])
def students_registered(cno):
    
    reg_students=Allocation.query.filter_by(course_id=cno).all()
        # course = Courses.query.get(course_id)
    student = [Students.query.get(allocation.student_id) for allocation in reg_students]

    cname=Courses.query.filter_by(course_id=cno).first()
    return render_template('students_registered.html',params=params,student=student , cname=cname)

if __name__ == '__main__':
    app.run(debug=True)