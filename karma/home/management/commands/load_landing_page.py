# from django.core.management.base import BaseCommand
# from home.models import (NavbarSection,HeaderSection,Banner, ServiceBox,
#                          TimeScheduleBox,TimeScheduleBoxTwo, About, AboutImage,
#                          sectionInfo,Service,AppoinmentSection,TestimonialSection,
#                          ClientSection,FooterSection)  

# class Command(BaseCommand):
#     help = 'Insert default data into NavbarSection'

#     def handle(self, *args, **kwargs):
#         # Check if already exists to avoid duplicates
#         try:
#             if NavbarSection.objects.exists():
#                 self.stdout.write(self.style.WARNING('NavbarSection data already exists.'))
#                 return
#             else:
#                 NavbarSection.objects.create(
#                     email='support@novena.com',
#                     address='Address Ta-134/A, New York, USA',
#                     number='823-4565-13456'
#                 )
#                 self.stdout.write(self.style.SUCCESS('NavbarSection data inserted successfully.'))

            
#             if HeaderSection.objects.exists():
#                 self.stdout.write(self.style.ERROR('HeaderSection already exist'))
#             else:
#                 HeaderSection.objects.create(
#                     title ='Novena',
#                     logo ='landingPage/header/logo.png'
#                 )
#                 self.stdout.write(self.style.SUCCESS('HeaderSection Data Inserted Successfully'))
            
#             if Banner.objects.exists():
#                 self.stdout.write(self.style.ERROR('Banner already exist'))
#             else:
#                 Banner.objects.create(
#                     title ='Total Health care solution',
#                     heading ='Your most trusted health partner',
#                     description ='A repudiandae ipsam labore ipsa voluptatum quidem quae laudantium quisquam aperiam maiores sunt fugit, deserunt rem suscipit placeat.',
#                     image ='landingPage/banner/slider-bg-1'
#                 )
#                 self.stdout.write(self.style.SUCCESS('Banner Data Inserted Successfully'))
            
#             if ServiceBox.objects.exists():
#                 self.stdout.write(self.style.ERROR('ServiceBox already exist'))
#             else:
#                 ServiceBox.objects.create(
#                     icon ='icofont-surgeon-alt',
#                     title ='24 Hours Service',
#                     heading ='Online Appoinment',
#                     description ='Get ALl time support for emergency.We have introduced the principle of family medicine.',
                  
#                 )
#                 self.stdout.write(self.style.SUCCESS('ServiceBox Data Inserted Successfully'))
            
#             if TimeScheduleBox.objects.exists():
#                 self.stdout.write(self.style.ERROR('TimeScheduleBox already exist'))
#             else:
#                 TimeScheduleBox.objects.create(
#                     icon ='icofont-ui-clock',
#                     title ='Timing schedule',
#                     heading ='Working Hours',
                  
#                 )
#                 self.stdout.write(self.style.SUCCESS('TimeScheduleBox Data Inserted Successfully'))
            
#             if TimeScheduleBoxTwo.objects.exists():
#                 self.stdout.write(self.style.ERROR('TimeScheduleBoxTwo already exist'))
#             else:
#                 data = [
#                     {"day_range": "Sun - Wed :", "time_range": "8:00 - 17:00"},
#                     {"day_range": "Thu - Fri :", "time_range": "9:00 - 17:00"},
#                     {"day_range": "Sat - sun :", "time_range": "10:00 - 17:00"},
#                 ]
#                 TimeScheduleBoxTwo.objects.bulk_create([
#                     TimeScheduleBoxTwo(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('TimeScheduleBoxTwo Data Inserted Successfully'))
            
#             if About.objects.exists():
#                 self.stdout.write(self.style.ERROR('About already exist'))
#             else:
#                 About.objects.create(
#                     title ='Personal care & healthy living',
#                     description ='We provide best leading medicle service Nulla perferendis veniam deleniti ipsum officia dolores repellat laudantium obcaecati neque.',
                  
#                 )
#                 self.stdout.write(self.style.SUCCESS('About Data Inserted Successfully'))
            
#             if AboutImage.objects.exists():
#                 self.stdout.write(self.style.ERROR('AboutImage already exist'))
#             else:
#                 data=[
#                     {'image':'landingPage/services/img-1.jpg'},
#                     {'image':'landingPage/services/img-2.jpg'},
#                     {'image':'landingPage/services/img-3.jpg'},
#                 ]
#                 AboutImage.objects.bulk_create([
#                     AboutImage(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('AboutImage Data Inserted Successfully'))
            
#             if sectionInfo.objects.exists():
#                 self.stdout.write(self.style.ERROR('sectionInfo already exist'))
#             else:
#                 data=[
#                     {'name':'service','title':'Award winning patient care','description':'Lets know moreel necessitatibus dolor asperiores illum possimus sint voluptates incidunt molestias nostrum laudantium. Maiores porro cumque quaerat.'},
#                     {'name':'testimonial','title':'We served over 5000+ Patients','description':'Lets know moreel necessitatibus dolor asperiores illum possimus sint voluptates incidunt molestias nostrum laudantium. Maiores porro cumque quaerat.'},
#                     {'name':'client','title':'Partners who support us','description':'Lets know moreel necessitatibus dolor asperiores illum possimus sint voluptates incidunt molestias nostrum laudantium. Maiores porro cumque quaerat.'},
#                 ]
#                 sectionInfo.objects.bulk_create([
#                     sectionInfo(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('sectionInfo Data Inserted Successfully'))
                
#             ##### Services Start ######
#             if Service.objects.exists():
#                 self.stdout.write(self.style.ERROR('Service already exist'))
#             else:
#                 data=[
#                     {'icon':'icofont-laboratory','title':'Laboratory services','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque'},
#                     {'icon':'icofont-heart-beat-alt','title':'Heart Disease','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque.'},
#                     {'icon':'icofont-tooth','title':'Dental Care','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque.'},
#                     {'icon':'icofont-crutch','title':'Body Surgery','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque.'},
#                     {'icon':'icofont-brain-alt','title':'Neurology Sargery','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque.'},
#                     {'icon':'icofont-dna-alt-1','title':'Gynecology','description':'Saepe nulla praesentium eaque omnis perferendis a doloremque.'},
#                 ]
#                 Service.objects.bulk_create([
#                     Service(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('Service Data Inserted Successfully'))
                
#             ###### APPOINMENT SECTION ######
#             if AppoinmentSection.objects.exists():
#                 self.stdout.write(self.style.ERROR('AppoinmentSection already exist'))
#             else:
#                 AppoinmentSection.objects.create(
#                     image ='landingPage/appoinment/img-3',
#                     title ='Book appoinment',
#                     number ='23 345 67980',
#                     description ='Mollitia dicta commodi est recusandae iste, natus eum asperiores corrupti qui velit . Iste dolorum atque similique praesentium soluta.',
                  
#                 )
#                 self.stdout.write(self.style.SUCCESS('AppoinmentSection Data Inserted Successfully'))
        
                
#             ###### TESTIMONIAL SECTION ######
#             if TestimonialSection.objects.exists():
#                 self.stdout.write(self.style.ERROR('TestimonialSection already exist'))
#             else:
#                 data=[
#                     {'image':'landingPage/testimonial/test-thumb1.jpg','title':'Amazing service!','occupation':'John Partho','description':'They provide great service facilty consectetur adipisicing elit.Itaque rem, praesentium, iure, ipsum magnam deleniti a vel eosadipisci suscipit fugit placeat.'},
#                     {'image':'landingPage/testimonial/test-thumb2.jpg','title':'Expert doctors!','occupation':'Mullar Sarth','description':' They provide great service facilty consectetur adipisicing elit.Itaque rem, praesentium, iure, ipsum magnam deleniti a vel eosadipisci suscipit fugit placeat.'},
#                     {'image':'landingPage/testimonial/test-thumb3.jpg','title':'Good Support!','occupation':'Kolis Mullar','description':'They provide great service facilty consectetur adipisicing elitItaque rem, praesentium, iure, ipsum magnam deleniti a vel eosadipisci suscipit fugit placeat.'},
#                     {'image':'landingPage/testimonial/test-thumb4.jpg','title':'Nice Environment!','occupation':'Partho Sarothi','description':'They provide great service facilty consectetur adipisicing elitItaque rem, praesentium, iure, ipsum magnam deleniti a vel eosadipisci suscipit fugit placeat.'},
#                     {'image':'landingPage/testimonial/test-thumb1.jpg','title':'Modern Service!','occupation':'Kolis Mullar','description':'They provide great service facilty consectetur adipisicing elitItaque rem, praesentium, iure, ipsum magnam deleniti a vel eosadipisci suscipit fugit placeat.'},
                    
#                 ]
#                 TestimonialSection.objects.bulk_create([
#                     TestimonialSection(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('TestimonialSection Data Inserted Successfully'))
                
#             ###### CLIENT SECTION ######
#             if ClientSection.objects.exists():
#                 self.stdout.write(self.style.ERROR('ClientSection already exist'))
#             else:
#                 data=[
#                     {'image':'landingPage/client/1.jpg'},
#                     {'image':'landingPage/client/2.jpg'},
#                     {'image':'landingPage/client/3.jpg'},
#                     {'image':'landingPage/client/4.jpg'},
#                     {'image':'landingPage/client/5.jpg'},
#                     {'image':'landingPage/client/6.jpg'},
#                     {'image':'landingPage/client/3.jpg'},
#                     {'image':'landingPage/client/4.jpg'},
#                     {'image':'landingPage/client/5.jpg'},
#                     {'image':'landingPage/client/6.jpg'},
                    
#                 ]
#                 ClientSection.objects.bulk_create([
#                     ClientSection(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('ClientSection Data Inserted Successfully'))
                
#             ###### FOOTER SECTION ######
#             if FooterSection.objects.exists():
#                 self.stdout.write(self.style.ERROR('FooterSection already exist'))
#             else:
#                 data=[
#                     {'logo':'landingPage/footer/logo.png','support':'Support Available for 24/7','email':'Support@email.com',
#                      'timing':'Mon to Fri : 08:30 - 18:00','number':'23-456-6588','description':'Tempora dolorem voluptatum nam vero assumenda voluptate, facilis ad eos obcaecati tenetur veritatis eveniet distinctio possimus.','facebook_url':'https://www.facebook.com/',
#                      'twitter_url':'https://www.facebook.com/','linkedin_url':'https://www.linkedin.com/'}
                    
#                 ]
#                 FooterSection.objects.bulk_create([
#                     FooterSection(**item) for item in data
#                 ])
#                 self.stdout.write(self.style.SUCCESS('FooterSection Data Inserted Successfully'))
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
#         except Exception as e:
#             self.stdout.write(self.style.ERROR(str(e)))