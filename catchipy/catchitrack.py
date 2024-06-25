from live.classes.track import Track
from typing import Optional
from live.classes.clip import Clip


class CatchiTrack(Track):
    def __init__(self, track: Track):
        self._track = track

    def __getattr__(self, item: str):
        """Return the attribute from the wrapped track.
        """
        return getattr(self._track, item)

    def set_clip(self, clip: Optional[Clip], clip_index: int = 0):
        """Set the clip in the given index.
        If the clip already exists in the given index, it will be deleted first.

        Args:
            clip: The clip to set
            clip_index: The index of the clip slot
        """
        if clip is not None and self.clips[clip_index] is not None:
            self._track.delete_clip(clip_index)

        self._track.create_clip(clip_index, clip.length)
        self._track.clips[clip_index] = clip