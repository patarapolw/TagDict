# TagDict

Let's create a taggable dictionary...

This project is based on `jupyter notebook` to view and edit `*.xls` and `*.ods` files.

I intend to create a comprehensive medical dictionary, which is searchable by tags and regex; and convertible to flashcards for apps like Anki, Memrise or Kitsun.io

## Usage

In Jupyter notebook,

```pydocstring
>>> from TagDict import TagDict
>>> med_dict = TagDict("medical_dict.ods")
>>> med_dict.view("blastoma")
A table about 'blastoma' is shown.
>>> med_dict.add(
        'glioblastoma',
        'Astrocytoma, pseudo-palisading',
        additional_keywords=['astrocytoma'],
        tags=['neurology']
    )
An updated table about 'glioblastoma' is shown.
```

## Screenshots

<img src="https://github.com/patarapolw/TagDict/tree/master/screenshots/0.png">
