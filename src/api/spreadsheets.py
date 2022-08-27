import collections

from fastapi import APIRouter, Body, Depends

import models
from api.dependencies import get_event_channels
from services import logger
from services.database_api import Units
from services.event_channels import EventChannels

router = APIRouter(prefix='/spreadsheets')


@router.post('/')
async def handle_events(
        worksheets_events: list[models.WorksheetEvents] = Body(),
        event_channels: EventChannels = Depends(get_event_channels),
):
    errors = collections.defaultdict(list)
    for worksheet_events in worksheets_events:
        try:
            unit = await Units.get_by_name(worksheet_events.worksheet_name)
        except KeyError:
            errors['unit_names'].append(worksheet_events.worksheet_name)
            logger.warning(f'Invalid unit name {worksheet_events.worksheet_name}')
        else:
            for event in worksheet_events.events:
                await event_channels.broadcast(models.Event(data={'unit_id': unit.id}, event_type=event))
                logger.debug(f'New event {event.name} {unit.name}')
    return {'errors': errors}
