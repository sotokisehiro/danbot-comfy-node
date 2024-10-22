from ..models.utils import ModelWrapper, normalize_tag_text
from ..models import v1, v2, v3
from .type import DART_MODEL_TYPE

STRING_OPTIONS = {
    "multiline": True,
}

COPYRIGHT_OPTIONS = {
    **STRING_OPTIONS,
    "placeholder": "copyright tags (e.g. vocaloid, ...)",
    "tooltip": "Comma separated tags that are categorized as copyright in danbooru",
}
CHARACTER_OPTIONS = {
    **STRING_OPTIONS,
    "placeholder": "character tags (e.g. hatsune miku, ...)",
    "tooltip": "Comma separated tags that are categorized as character in danbooru",
}
INPUT_TAGS_OPTIONS = {
    **STRING_OPTIONS,
    "placeholder": "general tags (e.g. 1girl, solo, ...)",
    "tooltip": "Comma separated tags. This will be the condition for upsampling tags. copyright/character tags in this field will be automatically detected the and merged",
}


class FormatterNodeMixin:
    def __init__(self):
        pass

    RETURN_TYPES = ("STRING", "STRING", "STRING", "STRING")
    RETURN_NAMES = ("formatted_prompt", "copyright", "character", "input_tags")

    FUNCTION = "format"

    OUTPUT_NODE = False

    CATEGORY = "prompt/Danbooru Tags Transformer"


class V1FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v1 model. This node deos not compatible with the v2 and v3 models."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (DART_MODEL_TYPE,),
                "rating": (
                    ["auto"] + list(v1.V1_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v1.V1_LENGTH_MAP.keys()),
                    {
                        "default": "long",
                    },
                ),
                "copyright": (
                    "STRING",
                    {
                        **COPYRIGHT_OPTIONS,
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **CHARACTER_OPTIONS,
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                    },
                ),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        rating: str,
        length: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v1.V1_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "rating": rating_tag,
                "length": v1.V1_LENGTH_MAP[length],
            }
        )
        return (prompt, copyright_tags, character_tags, condition_tags)


class V2FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v2 model. This node deos not compatible with the v1 and v3 models."

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (DART_MODEL_TYPE,),
                "aspect_ratio": (
                    list(v2.V2_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    ["auto"] + list(v2.V2_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v2.V2_LENGTH_MAP.keys()),
                    {
                        "default": "medium",
                    },
                ),
                "identity": (
                    list(v2.V2_IDENTITY_MAP.keys()),
                    {
                        "default": "none",
                    },
                ),
                "copyright": (
                    "STRING",
                    {
                        **COPYRIGHT_OPTIONS,
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **CHARACTER_OPTIONS,
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                    },
                ),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        aspect_ratio: str,
        rating: str,
        length: str,
        identity: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v2.V2_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "aspect_ratio": v2.V2_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v2.V2_LENGTH_MAP[length],
                "identity": v2.V2_IDENTITY_MAP[identity],
            }
        )
        return (prompt, copyright_tags, character_tags, condition_tags)


class V3FormatterNode(FormatterNodeMixin):
    DESCRIPTION = "Formats a prompt for a Dart v3 model. This node deos not compatible with the v1 and v2 models."

    EXPERIMENTAL = True

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "model": (DART_MODEL_TYPE,),
                "aspect_ratio": (
                    list(v3.V3_ASPECT_RATIO_MAP.keys()),
                    {
                        "default": "tall",
                    },
                ),
                "rating": (
                    ["auto"] + list(v3.V3_RATING_MAP.keys()),
                    {
                        "default": "general",
                    },
                ),
                "length": (
                    list(v3.V3_LENGTH_MAP.keys()),
                    {
                        "default": "medium",
                    },
                ),
                "copyright": (
                    "STRING",
                    {
                        **COPYRIGHT_OPTIONS,
                    },
                ),
                "character": (
                    "STRING",
                    {
                        **CHARACTER_OPTIONS,
                    },
                ),
                "input_tags": (
                    "STRING",
                    {
                        **INPUT_TAGS_OPTIONS,
                        "placeholder": "general and meta tags (e.g. 1girl, solo, ...)",
                    },
                ),
            },
        }

    def format(
        self,
        model: ModelWrapper,
        aspect_ratio: str,
        rating: str,
        length: str,
        copyright: str,
        character: str,
        input_tags: str,
    ):
        parsed = model.parse_prompt(input_tags, escape_brackets=False)

        copyright_tags = normalize_tag_text(", ".join([copyright, parsed.copyright]))
        character_tags = normalize_tag_text(", ".join([character, parsed.character]))
        condition_tags = parsed.known

        rating_tag = v3.V3_RATING_MAP[parsed.rating if rating == "auto" else rating]

        prompt = model.format_prompt(
            {
                "copyright": copyright_tags,
                "character": character_tags,
                "condition": condition_tags,
                "aspect_ratio": v3.V3_ASPECT_RATIO_MAP[aspect_ratio],
                "rating": rating_tag,
                "length": v3.V3_LENGTH_MAP[length],
            }
        )
        return (prompt, copyright_tags, character_tags, condition_tags)
