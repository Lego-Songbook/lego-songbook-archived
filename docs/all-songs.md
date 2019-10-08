---
layout: page
title: 所有音乐
permalink: /all-songs/
---

{% assign song_by_name = site.data.songs | sort: "name" %}
| Name | Key | Sheet |
|:---:|:---:|:---:|
{% for song in song_by_name -%}
| {{ song.name }} | {{ song.key }} | [{{ song.sheet_type }}]( {{ song.sheet_link }}) |
{% endfor %}
