import sys
import fileinput
from classes import Processor
from classes import Confession
from classes import ConfessionContainer
from classes import Classification
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn import svm

def main():
    all_text = ""
    try:
        for line in fileinput.input(sys.argv[1]):
            all_text += line
    except:
        print("error in input commands")

# ----------------------------------
    """
    Creates an instance of the formatter and process the lines
    """
    p = Processor(text=all_text)
    confessions = p.get_confessions()

    # for confession in confessions:
    #     print(confession.classification)

    #PREP DATA
    training, test = train_test_split(confessions, test_size=0.25, random_state=50)

    # print(len(training))
    # print(len(test))
    training_container = ConfessionContainer(training)
    testing_container = ConfessionContainer(test)

    ###supposed to evenly distribute for both. will do that later
    training_container.evenly_distribute()
    training_posts = training_container.get_all_posts()
    training_classifications = training_container.get_all_classifications()

    testing_container.evenly_distribute()
    testing_posts = testing_container.get_all_posts()
    testing_classifications = testing_container.get_all_classifications()


    #BAG OF WORDS VECTORIZATION
    vectorizer = TfidfVectorizer()

    training_posts_vectors = vectorizer.fit_transform(training_posts)
    testing_posts_vectors = vectorizer.transform(testing_posts)


    #CLASSIFICATION (linear SVM)
    svm_classifier = svm.SVC(kernel='linear')
    svm_classifier.fit(training_posts_vectors, training_classifications)


    # print("average number of reactions to posts this year is: %f" % p.get_avg_num_reactions())
    print("will your post get less than or greater than 100 reactions?")
    while True:
        pending_post = input("enter pending post: ")
        pp_as_list = [pending_post]
        pp_vectorize = vectorizer.transform(pp_as_list)
        print(svm_classifier.predict(pp_vectorize[0]))


    #EVALUATION


    # print(svm_classifier.score(testing_posts_vectors, testing_classifications))






if __name__ == "__main__":
    main()