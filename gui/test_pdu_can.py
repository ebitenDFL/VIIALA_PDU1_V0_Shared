#!/usr/bin/env python3
"""Hardware-independent tests for the GUI protocol helpers."""

import tempfile
import unittest
from pathlib import Path

from pdu_can import MCUBOOT_MAGIC, decode_i, decode_text, decode_u, inspect_update_image


class ProtocolHelpersTest(unittest.TestCase):
    def test_scalar_decoders(self):
        self.assertEqual(decode_u(b"\x8a\x01"), 0x018A)
        self.assertEqual(decode_i(b"\x9c\xff"), -100)
        self.assertEqual(decode_text(b"B001\0"), "B001")

    def test_valid_mcuboot_image(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "test.bin"
            payload = bytearray(512)
            payload[0:4] = MCUBOOT_MAGIC.to_bytes(4, "little")
            payload[100:104] = b"B001"
            image.write_bytes(payload)
            info = inspect_update_image(image)
            self.assertEqual(info["size"], 512)
            self.assertEqual(info["identity"], "B001")

    def test_rejects_plain_binary(self):
        with tempfile.TemporaryDirectory() as directory:
            image = Path(directory) / "bad.bin"
            image.write_bytes(b"not an mcuboot image" + bytes(64))
            with self.assertRaisesRegex(ValueError, "MCUboot"):
                inspect_update_image(image)


if __name__ == "__main__":
    unittest.main()
