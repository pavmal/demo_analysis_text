# Data Science
web demo of working model for text analysis and detect SPAM

Для полноценной работы модели анализа тональности отзывов необходимо:
 1. Установить библиотеку SpaCy:
pip install -U spacy
или
conda install -c conda-forge spacy

2. Загрузить мешок слов для требуемого языка
python -m spacy download en   # полный вариант (более 1 Гб)
или
python -m spacy download en_core_web_sm  # сокращенный вариант (~ 100 Мб)

