from faster_whisper import WhisperModel

whisper_model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)
