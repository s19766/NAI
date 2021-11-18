import argparse
import json

import imdb
import numpy as np

from compute_scores import euclidean_score


def build_arg_parser():
    parser = argparse.ArgumentParser(description='Find users who are similar to the input user')
    parser.add_argument('--user', dest='user', required=True,
                        help='Input user')
    return parser


# Finds users in the dataset that are similar to the input user
def find_similar_users(dataset, user, num_users):
    """
        Find similar users.
            Parameters:
                dataset (dict): File with data, json format
                user (str): User to compare
                num_users (int): Number of users

            Return:
                scores (dict): Return similar users

    """
    if user not in dataset:
        raise TypeError('Cannot find ' + user + ' in the dataset')

    # Compute Pearson score between input user
    # and all the users in the dataset
    scores = np.array([[x, euclidean_score(dataset, user,
                                           x)] for x in dataset if x != user])

    # Sort the scores in decreasing order
    scores_sorted = np.argsort(scores[:, 1])[::-1]

    # Extract the top 'num_users' scores
    top_users = scores_sorted[:num_users]

    return scores[top_users]


if __name__ == '__main__':
    args = build_arg_parser().parse_args()
    user = args.user
    #user = 'Paweł Czapiewski'

    ratings_file = 'dane.json'

    # Create connection to IMDB API
    ia = imdb.IMDb()

    with open(ratings_file, 'r', encoding="UTF-8") as f:
        data = json.loads(f.read())
    similar_users = find_similar_users(data, user, 16)

    best_match_movies = data[similar_users[0][0]]
    user_movies = data[user]
    diff_dict = {}

    for key in best_match_movies.keys():
        if key not in user_movies.keys():
            diff_dict[key] = best_match_movies[key]

    # Sorting dict by values
    diff_dict = {k: v for k, v in sorted(diff_dict.items(), key=lambda item: item[1], reverse=True)}

    print("\nResults for user " + user)
    recommended_movies = list(diff_dict.keys())[:5]
    print('\nRecommended movies : ')
    for i in recommended_movies:
        print('* ' + i)
        movies = ia.search_movie(i)
        movie = ia.get_movie(movies[0].movieID)
        print(' - year: ' + str(movie['year']))
        print(' - rating: ' + str(movie['rating']))
        print(' - votes: ' + str(movie['votes']))
        print(' - box office: ' + movie['box office']['Budget'])
        for director in movie['directors']:
            print(' - director: ' + director['name'])

    not_recommended_movies = list(reversed(diff_dict.keys()))[:5]
    print('\nNot recommended movies : ')
    for j in not_recommended_movies:
        print(' - ' + j)
