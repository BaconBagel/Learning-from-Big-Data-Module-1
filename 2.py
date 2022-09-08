import praw
import csv

comment_list = []


reddit = praw.Reddit(
    client_id="redacted",
    client_secret="redacted",
    user_agent="redacted",
)

reddit.read_only = True

for submission in reddit.subreddit("formula1").top(time_filter="week", limit=None):
    all_comments = submission.comments.list()
    print(all_comments)
    for comment in all_comments:
        try:
            body = comment.body
            flair = comment.author_flair_text
            upvotes = comment.score
            comment_id = comment.id
            comment_time = comment.created_utc
            body.replace(",", "")
            comment_list.append(body)
            comment_list.extend([flair])
            print(len(comment_list))
            with open('example.csv', 'a', encoding='utf-8') as file:
                if flair is not None:
                    fields = [str(comment_id), str(flair), str(body), str(upvotes), str(comment_time)]
                    writer = csv.writer(file)
                    writer.writerow(fields)
                    file.close()
        except AttributeError:
            print("error")

print(comment_list)
