from flask import Flask, render_template, request
from major.tf_idf import process_all_major_tf_idf, all_majors_word_tf_idf
from major.recommend import cal_user_input_rating, filter_result
from major.major_info_preprocess import major_name_mapping, major_info_original
from major.major_info_csv import major_info_dict, category_to_major


def algorithm_init():
    process_all_major_tf_idf()


algorithm_init()

app = Flask(__name__)


@app.route("/")
def getInput():
    return render_template('index.html')

@app.route('/home')
def home1():
    categories = [x for x in category_to_major.keys()]
    return render_template('home.html', categories=categories)

@app.route("/result", methods=['POST'])
def get_result():
    if request.method == 'POST':
        description = request.form.get('description', None)
        category = request.form.get('category', None)
        income = request.form.get('income')
        income = float(income) if income else 0

        print("description: {0} category: {1}, income {2}".format(description, category, income))

        # description = 'I like mathematics and physics a lot, want to do engineering works.'
        # category = request.form.get('category', None)
        # income = 0

        majors = cal_user_input_rating(description)
        majors = filter_result(majors,  income_threshold=income)
        majors = get_all_major_info(majors)
        return render_template('result.html', majors=majors)


def get_all_major_info(res):
    majors = []
    for tmp in res:
        name = tmp[0]
        name = major_name_mapping[name]
        info = major_info_original[name]
        major = dict(
            name=name,
            rating=tmp[1],
            category=major_info_dict[tmp[0]]['category'],
            income=major_info_dict[tmp[0]]['income'],
            info=info
        )
        majors.append(major)
        print('{0}, rating: {1}, category: {2}, income: {3}:\n{4}\n***********'
              .format(name, tmp[1], major_info_dict[tmp[0]]['category'], major_info_dict[tmp[0]]['income'], info))
    return majors


if __name__ == '__main__':
    algorithm_init()
    app.run(debug = True)
