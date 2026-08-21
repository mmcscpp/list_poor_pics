import unittest


TOLERANCE = 0


class Axes:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height + 1

    def resolution(self) -> int:
        return self.width * self.height

    def ratio(self) -> float:
        if self.height > self.width:
            return self.height / self.width
        return self.width / self.height

    def __str__(self) -> str:
        return f"{self.width}x{self.height}"

    def __eq__(self, cmp_axes: object) -> bool:
        if isinstance(cmp_axes, Axes):
            return self.width == cmp_axes.width and self.height == cmp_axes.height
        return False

    def __lt__(self, cmp_axes: object) -> bool:
        """ return true if both axes are lower than the passed 'compareWith'-axes """
        if not isinstance(cmp_axes, Axes):
            return False

        if self.height > self.width:
            left_x_axis = self.height
            left_y_axis = self.width
        else:
            left_x_axis = self.width
            left_y_axis = self.height

        right_x_axis = cmp_axes.width - TOLERANCE
        right_y_axis = cmp_axes.height - TOLERANCE

        conde = left_x_axis != right_x_axis or left_y_axis != right_y_axis
        condx = left_x_axis <= right_x_axis
        condy = left_y_axis <= right_y_axis
        result = conde and condx and condy
        # print(f"condx={condx}, condy={condy} -> result={result} - self={self.width}x{self.height} < {compareWith}")
        return result


class AxesTest(unittest.TestCase):

    def set_up(self) -> None:
        self.limit_axes = Axes(1200, 900)
        # 1st change for feature-3 branch
        print(f"limit_axes={self.limit_axes}")

    def test_axes_lt_1(self) -> None:
        test_axes = [(Axes(500, 300), True), (Axes(300, 500), True), \
                     (Axes(500, 1200), True), (Axes(900, 755), True), \
                     (Axes(1200, 900), False), \
                     (Axes(2400, 1224), False), (Axes(1224, 2400), False), (Axes(900, 1300), False), \
                     (Axes(500, 900), True), (Axes(900, 500), True), \
                     (Axes(1400, 600), False), (Axes(600, 1400), False)]

        for axes, expected in test_axes:
            # result = axes < self.limit_axes
            # print(f"{axes} < {self.limit_axes} = {result}  --> expected={expected}")
            # self.assertEqual(result, expected)
            self.assertEqual((axes < self.limit_axes), expected)

    def test_xxes_lt_2a(self) -> None:
        test_axes = Axes(800, 748)

        self.assertEqual(test_axes < Axes(900, 675), False)
        self.assertEqual(test_axes < Axes(960, 720), False)
        self.assertEqual(test_axes < Axes(1200, 900), True)

    def test_axes_lt_2b(self) -> None:
        test_axes = Axes(750, 1000)

        self.assertEqual(test_axes < Axes(900, 675), False)
        self.assertEqual(test_axes < Axes(960, 720), False)
        self.assertEqual(test_axes < Axes(1200, 900), True)

    def test_axes_lt_3(self) -> None:
        test_axes = [(Axes(1195, 895), True), \
                     (Axes(1200, 900), False), \
                     (Axes(1205, 905), False)]
        for axes, expected in test_axes:
            self.assertEqual((axes < self.limit_axes), expected)

    def tear_down(self) -> None:
        self.test_axes = None


if __name__ == "__main__":
    unittest.main(exit=True)
