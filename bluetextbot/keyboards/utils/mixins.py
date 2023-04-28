class KeyboardMarkupMixin():
    def to_python(self) -> dict:
        return self._build().to_python()

    async def row(self, row: "ButtonRow") -> None:  # type: ignore
        self.rows.append(row)

    async def add(self, button: "KeyboardButton") -> None:  # type: ignore
        self.rows[-1].append(button)

    async def remove(self, index: int = 0) -> None:
        self.rows.pop(index)
