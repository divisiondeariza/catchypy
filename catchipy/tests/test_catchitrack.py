import re
from unittest.mock import MagicMock
from catchipy.catchitrack import CatchiTrack
import pytest
from live.classes.track import Track

@pytest.fixture
def track() -> MagicMock:
    """ 
    Return a MagicMock of a Track object.
    """
    track = MagicMock()
    track.clips = [MagicMock() for _ in range(4)]
    return track

@pytest.fixture
def catchi_track(track: MagicMock) -> CatchiTrack:

    return CatchiTrack(track)


class TestCatchiTrack:
    """
    Unit tests for the CatchiTrack class.
    """

    def test_getattr(self, catchi_track: CatchiTrack, track: MagicMock) -> None:
        """
        Test that __getattr__ returns the attribute from the wrapped track.
        """
        assert catchi_track.clips == track.clips

    def test_set_clip(self, catchi_track: CatchiTrack, track: MagicMock) -> None:
        """
        Test that set_clip deletes the existing clip if it exists and creates a new clip in the given index.
        """
        clip = MagicMock()
        clip_index = 0
        catchi_track.set_clip(clip, clip_index)
        track.delete_clip.assert_called_with(clip_index)
        track.create_clip.assert_called_with(clip_index, clip.length)
        assert track.clips[clip_index] == clip

    def test_set_clip_with_non_existing_clip(self, catchi_track: CatchiTrack, track: MagicMock) -> None:
        """
        Test that set_clip creates a new clip in the given index if the existing clip is None.
        """
        clip = MagicMock()
        clip_index = 0
        track.clips[clip_index] = None
        catchi_track.set_clip(clip, clip_index)
        track.delete_clip.assert_not_called()
        track.create_clip.assert_called_with(clip_index, clip.length)
        assert track.clips[clip_index] == clip
