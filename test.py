from underthesea import word_tokenize, ner

# Ví dụ bài thơ có địa danh
poem = "Đừng lặng im"

# Tokenize và nhận diện thực thể
tokens = word_tokenize(poem)
entities = ner(poem)

print("Tokens:", tokens)
print("Entities:", entities)