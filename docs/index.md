---
# Feel free to add content and custom Front Matter to this file.
# To modify the layout, see https://jekyllrb.com/docs/themes/#overriding-theme-defaults

layout: default
title: Lego Songbook
---

## 目录

+ [所有音乐](#所有音乐)
    - [按字母顺序](#按字母顺序)
    - [按调式](#按调式)
    - [按唱的频率](#按唱的频率)
+ [以往敬拜](#以往敬拜)
    - [主日敬拜](#主日敬拜)
    - [特殊活动](#特殊活动)


## 所有音乐

### 按字母顺序

[回到目录](#目录)

{% assign songs_by_name = site.data.songs | sort: "name" %}
{% for song in songs_by_name %}
{{ song.name }} {{ song.key }} [{{ song.sheet_type }}]({{ song.sheet_link }})
{% endfor %}

### 按调式

[回到目录](#目录)

{% assign all_keys = "C, C#, D, Eb, E, F, F#, G, Ab, A, Bb, B" | split: ", " %}
{%- for key in all_keys -%}
    {%- assign song_in_key = site.data.songs | where: "key", key -%}
    {%- if song_in_key.size != 0 -%}
        [{{ key }}](${{ key }}) -
    {% endif -%}
{%- endfor -%}

{% for key in all_keys %}
{% assign song_in_key = site.data.songs | where: "key", key %}
{% if song_in_key.size != 0 %}

#### {{ key}}

{% for song in song_in_key %}
{{ song.name }} {{ song.key }} [{{ song.sheet_type }}]({{ song.sheet_link }})
{% endfor %}

{% endif %}
{% endfor %}


### 按唱的频率

[回到目录](#目录)

## 以往敬拜

[回到目录](#目录)

### 主日敬拜

[回到目录](#目录)

{% for service in site.data.past_services %}

#### {{ service.date }}

+ 带领人: {{ service.lead_singer }}
{%- if service.vocals %}
+ 伴唱: {{ service.vocals }}
{%- endif %}
{%- if service.instrumentation %}
+ 乐器:
{%- for instrument in service.instrumentation %}
    - {{ instrument.instrument }}: {{ instrument.player }}
{%- endfor -%}
{%- endif %}
+ 曲目:
{%- for song in service.songs -%}
{%- assign this_song = site.data.songs | where: "name", song -%}
{%- if this_song.first %}
    - [{{ song }}]({{ this_song.first.sheet_link }})
{%- else %}
    - {{ song }}
{%- endif -%}
{%- endfor -%}
{%- endfor %}

### 特殊活动

#### 十一营会（2019年10月2日～2019年10月4日）
