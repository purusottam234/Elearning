from django.db import models
from django.core.exceptions import ObjectDoesNotExist

class OrderField(models.PositiveIntegerField):
    def __init__(self,for_fields=None,*args,**kwargs):
        self.for_fields = for_fields
        super().__init__(*args,**kwargs)
        
    def pre_save(self, model_instance, add):
        '''
        this method override the pre_save method of positiveIntegerfield before saving to database

       here we perform the following actions:
       i. check whether value is already exists for the fields in the model instance
       a.we retrieve the all objects for the field in the model instance
       b.if there are any fields names in the for_fields attribute of the field
       c.we retrieve the object with highest order with last_item = qs.latest(self.attname),if no object is found,we assume
       this object as first one and assign the order 0 to it
       d. if object found , add 1 to the highest order found
       e. we assign the calculated order to field's value in the models instance using setattr() and
       return it
       ii.if model instance has a value for the current field , you it insted of calculating it
        '''
        if getattr(model_instance,self.attname) is None:
            try:
                qs = self.model.objects.all()
                if self.for_fields:
                    query = {field:getattr(model_instance,field)\
                             for field in self.for_fields}
                    qs = qs.filter(**query)
                last_item = qs.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance,self.attname,value)
            return value
        else:
            return super().pre_save(model_instance,add)