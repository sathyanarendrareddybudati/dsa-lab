#!/usr/bin/env python3
def analyze_friend_request(message):

    upper_count = 0
    punct_count = 0
    alpha_count = 0
    is_spam = False
    consecutive_count = 1

    for i in range(len(message)):
        char = message[i]

        if char.isalpha():
            alpha_count += 1
            if char.isupper():
                upper_count += 1

        if char in ("!", "?"):
            punct_count += 1

        if i > 0:
            if char == message[i - 1]:
                consecutive_count += 1
                if consecutive_count > 3:
                    is_spam = True
            else:
                consecutive_count = 1

    caps_ratio = upper_count / alpha_count if alpha_count > 0 else 0

    if caps_ratio >= 0.6 or punct_count >= 5:
        classification = "AGGRESSIVE"
    elif caps_ratio >= 0.3 or punct_count >= 3:
        classification = "URGENT"
    else:
        classification = "CALM"

    return classification, is_spam


test_cases = ["Hey, want to connect?", "PLEASE ACCEPT MY REQUEST!!!", "Are you free? I need to talk!!!"]

print(f"{'Message':<15} | {'Status':<12} | {'Spam'}")
print("-" * 40)
for msg in test_cases:
    status, spam = analyze_friend_request(msg)
    print(f"{msg:<15} | {status:<12} | {spam}")
