# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.

import matplotlib.pyplot as plt
import numpy as np
import shortuuid
import os
import urllib.parse
import urllib.request
import base64
import json
from datatypes_date_time.timex import Timex

from botbuilder.dialogs import WaterfallDialog, WaterfallStepContext, DialogTurnResult
from botbuilder.dialogs.prompts import ConfirmPrompt, TextPrompt, PromptOptions
from botbuilder.core import MessageFactory
from botbuilder.schema import (
    ActivityTypes,
    Attachment,
    AttachmentData,
    Activity)
from .cancel_and_help_dialog import CancelAndHelpDialog


class PlotDialog(CancelAndHelpDialog):
    def __init__(self, dialog_id: str = None):
        super(PlotDialog, self).__init__(
            dialog_id or PlotDialog.__name__)
        self.add_dialog(
            WaterfallDialog(
                WaterfallDialog.__name__,
                [
                    self.create_plot_step,
                    self.final_step,
                ],
            )
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def create_plot_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Create Plot.
        :param step_context:
        :return DialogTurnResult:
        """

        imgId = shortuuid.uuid()
        self._create_fancy_plot(imgId)

        reply = Activity(type=ActivityTypes.message)
        reply.text = "This is a fancy Plot:"
        reply.attachments = [self._get_inline_attachment(imgId)]
        await step_context.context.send_activity(reply)

        os.remove(imgId + ".png")

        return await step_context.next(step_context.result)

    async def final_step(self, step_context: WaterfallStepContext) -> DialogTurnResult:
        """
        Complete the interaction and end the dialog.
        :param step_context:
        :return DialogTurnResult:
        """
        return await step_context.end_dialog()

    def _create_fancy_plot(self, id):
        def f(t):
            return np.exp(-t) * np.cos(2*np.pi*t)

        t1 = np.arange(0.0, 5.0, 0.1)
        t2 = np.arange(0.0, 5.0, 0.02)

        plt.figure()
        plt.subplot(211)
        plt.plot(t1, f(t1), 'bo', t2, f(t2), 'k')

        plt.subplot(212)
        plt.plot(t2, np.cos(2*np.pi*t2), 'r--')
        plt.savefig(id + '.png')

    def _get_inline_attachment(self, id) -> Attachment:
        """
        Creates an inline attachment sent from the bot to the user using a base64 string.
        Using a base64 string to send an attachment will not work on all channels.
        Additionally, some channels will only allow certain file types to be sent this way.
        For example a .png file may work but a .pdf file may not on some channels.
        Please consult the channel documentation for specifics.
        :return: Attachment
        """
        file_path = os.path.join(
            os.getcwd(), id + ".png")
        with open(file_path, "rb") as in_file:
            base64_image = base64.b64encode(in_file.read()).decode()

        return Attachment(
            name="architecture-resize.png",
            content_type="image/png",
            content_url=f"data:image/png;base64,{base64_image}",
        )
