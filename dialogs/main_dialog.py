# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
    DialogTurnStatus,
)
from botbuilder.core import MessageFactory
from botbuilder.schema import ActivityTypes, InputHints

from dialogs.plot_dialog import PlotDialog


class MainDialog(ComponentDialog):
    """
    A root dialog that can route activities sent to the skill to different sub-dialogs.
    """

    def __init__(self):
        super().__init__(MainDialog.__name__)
        self.add_dialog(PlotDialog())
        self.add_dialog(
            WaterfallDialog(WaterfallDialog.__name__, [self.process_activity])
        )

        self.initial_dialog_id = WaterfallDialog.__name__

    async def process_activity(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        current_activity_type = step_context.context.activity.type

        # A skill can send trace activities, if needed.
        await step_context.context.send_trace_activity(
            f"{MainDialog.__name__}.process_activity()",
            label=f"Got ActivityType: {current_activity_type}",
        )

        if current_activity_type == ActivityTypes.event:
            return await self._on_event_activity(step_context)
        if current_activity_type == ActivityTypes.message:
            return await self._on_message_activity(step_context)
        if current_activity_type == ActivityTypes.conversation_update:
            return await self._on_conversation_update_activity(step_context)
        else:
            # We didn't get an activity type we can handle.
            await step_context.context.send_activity(
                MessageFactory.text(
                    f'Unrecognized ActivityType: "{current_activity_type}".',
                    input_hint=InputHints.ignoring_input,
                )
            )
            return DialogTurnResult(DialogTurnStatus.Complete)

    async def _on_event_activity(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        This method performs different tasks based on the event name.
        """
        # We didn't get an activity name we can handle.
        await step_context.context.send_activity(
            MessageFactory.text(
                'Python Dialog Event happend',
                input_hint=InputHints.ignoring_input,
            )
        )
        return DialogTurnResult(DialogTurnStatus.Complete)

    async def _on_conversation_update_activity(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        This method performs different tasks based on the event name.
        """
        # We didn't get an activity name we can handle.
        await step_context.context.send_activity(
            MessageFactory.text(
                'Python Dialog Conversation Update happend',
                input_hint=InputHints.ignoring_input,
            )
        )
        return DialogTurnResult(DialogTurnStatus.Complete)

    async def _on_message_activity(
        self, step_context: WaterfallStepContext
    ) -> DialogTurnResult:
        """
        This method just gets a message activity.
        """

        plot_dialog = await self.find_dialog(PlotDialog.__name__)
        return await step_context.begin_dialog(plot_dialog.id)
