from craftgame.common.exceptions import AppError


class AiError(AppError):
    pass


class AiGenerationError(AiError):
    status = 500
    message = "ai generation error"
