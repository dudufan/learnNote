个人理解有以下优点：
支持字符串的长度校验、正则校验
支持 校验 类型，一个字段可以是一种或多种类型（object, list, string, number, integer)
支持数值校验范围
支持校验object有哪些字段必选
schema有助于明确接口入参, 也能更加直观地了解数据的内容。

标准化定义可以使得我们不需要在实际应用编写中增加额外的检测代码. schema.json配置文件比代码灵活



# 对json中child的校验
通过properties校验json中的每个child


# 校验array类型的字段
对孩子类型的校验是通过“item"进行嵌套。item中可以校验String Number，也可以 继续在item中嵌套properties字段继续校验 Json
```json
"tags": {

      "$id": "/properties/tags",

      "type": "array",

      "items": {

        "$id": "/properties/tags/items",

        "type": "string",

        "title": "The 0th Schema ",

        "default": "",

        "examples": [

          "home",

          "green"

        ]

      }

    }

```


# 完整示例
```json
{

  "$id": "http://example.com/example.json",

  "type": "object",

  "definitions": {},

  "$schema": "http://json-schema.org/draft-07/schema#",

  "properties": {

    "checked": {

      "$id": "/properties/checked",

      "type": "boolean",

      "title": "The Checked Schema ",

      "default": false,

      "examples": [

        false

      ]

    },

    "dimensions": {

      "$id": "/properties/dimensions",

      "type": "object",

      "properties": {

        "width": {

          "$id": "/properties/dimensions/properties/width",

          "type": "integer",

          "title": "The Width Schema ",

          "default": 0

        },

        "height": {

          "$id": "/properties/dimensions/properties/height",

          "type": "integer",

          "title": "The Height Schema ",

          "default": 0,

          "examples": [

            10

          ]

        }

      }

    },

    "id": {

      "$id": "/properties/id",

      "type": "integer",

      "title": "The Id Schema ",

      "default": 0,

      "examples": [

        1

      ]

    },

    "name": {

      "$id": "/properties/name",

      "type": "string",

      "title": "The Name Schema ",

      "default": "",

      "examples": [

        "A green door"

      ]

    },

    "price": {

      "$id": "/properties/price",

      "type": "number",

      "title": "The Price Schema ",

      "default": 0,

      "examples": [

        12.5

      ]

    },

    "tags": {

      "$id": "/properties/tags",

      "type": "array",

      "items": {

        "$id": "/properties/tags/items",

        "type": "string",

        "title": "The 0th Schema ",

        "default": "",

        "examples": [

          "home",

          "green"

        ]

      }

    }

  }

}





```