from axes import Axes


class PicSizeChecker:
    def __init__(self, limit_axes: Axes) -> None:
        self.limit_axes = limit_axes
        self.to_small_count = 0
        self.checked_pic_axes = Axes(99999, 99999)
        self.smallest_pic_file_name = ""
        self.smallest_pic_resolution = self.checked_pic_axes.resolution()
        self.smallest_pic_axes = Axes(0, 0)

    def __str__(self) -> str:
        return f"{self.limit_axes}"

    def is_to_small(self, file_name: str, pic_axes: Axes) -> bool:
        # test if the picture is smaller than the limit axes
        smaller = False
        if pic_axes < self.limit_axes:
            self.to_small_count += 1
            smaller = True

        if pic_axes.width < self.checked_pic_axes.width:
            self.checked_pic_axes.width = pic_axes.width
        if pic_axes.height < self.checked_pic_axes.height:
            self.checked_pic_axes.height = pic_axes.height

        # find smallest picture
        resolution = pic_axes.resolution()
        if smaller and resolution < self.smallest_pic_resolution:
            self.smallest_pic_resolution = resolution
            self.smallest_pic_file_name = file_name
            self.smallest_pic_axes = pic_axes

        return smaller

    def check(self, file_name: str, pic_axes: Axes) -> bool:
        return self.is_to_small(file_name, pic_axes)

    def to_string(self) -> str:
        info = f"pics < {self.limit_axes}: {self.to_small_count}"
        if self.to_small_count > 0:
            info += f"; smallest pic: {self.smallest_pic_file_name} ({self.smallest_pic_axes})"
        return info


BAD_RATIO_THRESHOLD = 2.0


class PicRatioChecker:
    def __init__(self) -> None:
        self.bad_ratio_count = 0

    def has_bad_ratio(self, pic_axes: Axes) -> bool:
        bad_ratio = pic_axes.ratio() >= BAD_RATIO_THRESHOLD
        if bad_ratio:
            self.bad_ratio_count += 1
        return bad_ratio

    def check(self, file_name: str, pic_axes: Axes) -> bool:
        return self.has_bad_ratio(pic_axes)

    def to_string(self) -> str:
        info = f"pics with bad ratio: {self.bad_ratio_count}"
        return info
