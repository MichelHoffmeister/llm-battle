from team_a.story_bot import get_response as get_response_a
from team_b.story_bot import get_response as get_response_b


def generate_story(length=10):
    story = []

    end = False
    for i in range(length):
        if i == length - 1:
            end = True
        if i % 2 == 0:
            response_a = get_response_a(index=1+i, end=end, story=" ".join(story))
            story.append(response_a)
        else:
            response_b = get_response_b(index=1+i, end=end, story=" ".join(story))
            story.append(response_b)
    
    return story

story = generate_story()

print(story)

with open("story.txt", "w") as f:
    f.write("\n".join(story))