from django.db import models

class Trend(models.Model):
    """
    Model of trends based on collected data set 
    """
    TRL_OPTIONS = (('Pilot','Pilot'),('Development','Development'), ('Deploy','Deploy'))
    STEEPL_OPTIONS = (('S','S'),('T','T'),('E','E'),('P','P'),('L','L'))
    IMPACT_STRENGTH_OPTIONS = (('Low','Low'),('Medium','Medium'),('High','High'))

    megatrend = models.CharField(max_length=150)
    macrotrend = models.CharField(max_length=200)
    challenges_and_research_gaps = models.TextField()
    total_count_of_publications = models.PositiveIntegerField(null=True, blank=True)
    total_count_of_patents = models.PositiveIntegerField(null=True, blank=True)
    technology_readiness_level = models.CharField(choices=TRL_OPTIONS,max_length=50, blank=True, null=True)
    impact_strength = models.CharField(choices=IMPACT_STRENGTH_OPTIONS, max_length=50, default=IMPACT_STRENGTH_OPTIONS[0])
    steepl = models.CharField(choices=STEEPL_OPTIONS,max_length=10, default=STEEPL_OPTIONS[0])
    relevant_industries = models.TextField(blank=True, null=True)
    real_world_application_and_use_cases = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Megatrend: {self.megatrend} Macrotrend: {self.macrotrend} TRL: {self.technology_readiness_level}"