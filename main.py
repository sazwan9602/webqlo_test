# get required library
import json
from ast import literal_eval
from helper import filter_by_date, cleaned_df, get_interaction_summary
from datetime import datetime

# Start and end date as per instruction
start = "2020-06-01"
end = "2021-11-30"


def interactions():
    """
    Count total interaction of:
        Views
        Shares
        Reactions
        Comments
        Non Video Interaction
        All
    :return:
    """
    df = filter_by_date(start, end)
    total_views = df['video_views'].sum()

    shares = cleaned_df(df, 'shares')
    reactions = cleaned_df(df, 'reactions')
    comments = cleaned_df(df, 'comments')

    # convert dataframe into dictionary
    dict_share = shares['shares'].apply(literal_eval)
    dict_reactions = reactions['reactions'].apply(literal_eval)
    dict_comments = comments['comments'].apply(literal_eval)

    # count total using List Comprehension
    total_share = sum(e['count'] for e in dict_share)
    # normally people used to iterate list and do some calculations, by using python list comprehension you can get result in 1 line
    # here's an example for test_total using normal method
    test_total = 0
    for e in dict_share:
        test_total += e['count']
    # same result as total_share but test_total used 3 line of codes(wasted)
    total_reactions = sum(e['summary']['total_count'] for e in dict_reactions)
    total_comments = sum(e['summary']['total_count'] for e in dict_comments)

    # dict summary
    total_interactions = {
        'all': total_share + total_reactions + total_comments + int(total_views),
        'video_views': int(total_views),
        'non_video_interactions': total_comments + total_share + total_reactions,
        'shares': total_share,
        'reactions': total_reactions,
        'comments': total_comments
    }

    return total_interactions


def total_post():
    """
    Count total type of post and for each category
        - all
        - photo
        - video
        - link
        - and others....
    :return:
    """
    df = filter_by_date(start, end)
    filtered_df = cleaned_df(df, 'type')
    posts = filtered_df['type'].value_counts()

    sum_post = posts.sum()
    total = posts.to_dict()
    total['all'] = int(sum_post)

    return total


def interaction_by_type():
    """
    Summary for interaction by type:
        photo
        video
        others (exclude photo and video type)
    Each type consists of these fields:
        - id
        - name
        - count
        - interactions
    :return:
    """
    df = filter_by_date(start, end)
    filtered_df = cleaned_df(df, 'type')

    photo_df = filtered_df[filtered_df['type'].str.contains('photo')]
    video_df = filtered_df[filtered_df['type'].str.contains('video')]
    other_df = filtered_df[~filtered_df['type'].isin(['photo', 'video'])]

    # python Mapping: google this one, really useful and save a lot line of codes
    interaction_lists = list(map(get_interaction_summary, [photo_df, video_df, other_df]))

    return interaction_lists


if __name__ == "__main__":
    print("Start:", datetime.now())
    # convert to list
    data = [{
        'total_interactions': interactions(),
        'total_post': total_post(),
        'interactions_by_type': interaction_by_type()
    }]

    # convert to json
    with open('overall_summary.json', 'w') as outfile:
        json.dump({'data': data}, outfile, indent=4)

    print('Finish:', datetime.now())
    print('Json file created.')
