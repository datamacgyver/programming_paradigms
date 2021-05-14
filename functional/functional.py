# At first glance, functional looks like procedural but there is a key difference.
# *Side effects are banned* and *everything is immutable*

num = 1


def function_to_add_one(num):
    return num + 1


function_to_add_one(num)
function_to_add_one(num)
function_to_add_one(num)
function_to_add_one(num)
function_to_add_one(num)

print(num)
# Scroll down for more context
















# So here, when I run the function it always returns the same value because num cannot change without
# a new assignment. It is immutable. I should be designing my functions so that I don't have to use
# a state to get my results.
num = 1


def function_to_add_one(num, repetitions):
    return num + (1*repetitions)


out = function_to_add_one(num, 5)

print(out)
# Scroll down for more context




























# The above still isn't particularly functional. What we should really be doing is adopting a
# slightly different paradigm of recursive calls that do not require any assignment whatsoever:
num = 1


def function_to_add_one(num, repetitions):
    if repetitions == 1:
        return num + 1
    else:
        return function_to_add_one(num+1, repetitions-1)


out = function_to_add_one(num, 5)

print(out)
# Scroll down for more context
































# This idea of static state manifests in several ways. Python isn't really setup for
# functional coding but there are some features that are actually very similar. Let's
# now look at some list operations:

strings = ["a", "ab", "abc", "abcd"]
print(strings)

strings.append("abcdef")
print(strings)

strings.reverse()
print(strings)








# Note that, while I haven't done any assignments except for the first one, the list
# has changed at each step, I have modified its state which is a big no no in functional
# programming! Imagine I was doing this in a function, I wouldn't really know what state my
# string variable was in unless I checked which can make debugging hard!

# You can see this better if I do actually do this in functions (which is similar to our procedural
# paradigm)


def add_a_val(lst, val):
    lst.append(val)


def rev(lst):
    lst.reverse()


strings = ["a", "ab", "abc", "abcd"]
add_a_val(strings, "abcdef")
rev(strings)
print(strings)







# Luckily, Python has features to do this in a more functional context:
strings = ["a", "ab", "abc", "abcd"]
print(strings)

strings = strings + ["abcdef"]
print(strings)

strings = strings[::-1]
print(strings)

# Now, I am assigning new variables here *but I am not changing the old one*
# Instead I create a new one! The reason this looks odd is it still isn't functional











# Here's a more functional version, note I'm avoiding assignments, that's not going to always work
# but it should be the direction you are thinking. It's not *wrong* to create new variables (even
# mutable ones) in a function, but their context should be limited to that function only!


def add_a_val(lst, val):
    return lst + [val]


def create_new_list(lst):
    return add_a_val(lst, "abcdef")[::-1]


strings = ["a", "ab", "abc", "abcd"]
strings_out = create_new_list(strings)

print(strings_out)









# This is now where python's tooling comes into its own. List comprehension is the very essence
# of functional programming. It's a highly flexible map operation:
def replace_as(a_str):
    return a_str.replace("a", "z")

strings = ["a", "ab", "abc", "abcd"]
strings_out = [replace_as(s) for s in strings]

print(strings)
print(strings_out)


# Here, I have used list comprehension to create a new list with updated values. Note that the original
# list is unchanged and I have created a brand new one with the updated values rather than modifying them
# in place. This is functional and means you always know where you are with a variable.



# I actually think that Python has got this right, there are aspects of functional programming that are really useful,
# things like thinking before you use state are advantageous and being able to lean into immutability make multi-thread
# processes trivial to design but, not having to go all in on the representations such as my create_new_list() function
# when in actuall fact a bit of mutability would be easier to read is really handy!