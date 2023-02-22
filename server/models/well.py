from pydantic import BaseModel
from datetime import datetime

# pydantic will use different schemas for saving and loading models
# use something like wellInput, or wellCreate for creating models
# wellOutput or just well for showing


class Well(BaseModel):
	Id: int
	Name: str
	afe_number: str
	coring: str

	critical_date: str
	critical_date_type: str

	current_nri_oil: str
	current_wi: str

	div_defined_alpha_numeric_2: str

	drilling_duration: str
	drilling_end_dt: datetime
	drilling_start_dt: datetime

	entity_name: str
	exception_comments: str
	gg_prospect: str
	lateral_mileage: str
	logging: str
	paf_tracking: str
	permit_submit_date: str
	pilot_hole: str
	remarks: str

	resource_id: int
	resource_name: str

	stepout: str
	subtrend: str
	subtrend2: str
	target_spacing: str
	tier_name: str

	class Config:
			orm_mode = True
