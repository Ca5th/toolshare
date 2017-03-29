from django.test import TestCase
from datetime import datetime

from toolshareapp.models import Tool
from toolshareapp.models import ToolStatus
from toolshareapp.models import User
from toolshareapp.models import UserRole

from toolshareapp.services import ToolService

class ToolTest(TestCase):
    
    def test_tool_deactivated(self):        
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available)
        
        #2. Act
        tool.deactivate()
        
        #3. Assert
        self.assertEqual(False, tool.active, 'tool.active != False')
        
    def test_tool_unavailable(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available)
        
        #2. Act
        tool.make_unavailable()
        
        #3. Assert
        self.assertEqual(ToolStatus.Unavailable, tool.status, 'tool.status != ToolStatus.Unavailable')
        
    def test_tool_available(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Unavailable)
        
        #2. Act
        tool.make_available()
        
        #3. Assert
        self.assertEqual(ToolStatus.Available, tool.status, 'tool.status != ToolStatus.Available')
        
class ToolServiceTest(TestCase):
    
    def setUp(self):
        self.tool_service = ToolService()
        
        self.user = User.objects.create(name = 'test name',
                                        lastname = 'test lastname',
                                        zip_code = '11111',
                                        registration_date = datetime.now().date(),
                                        last_login_date = datetime.now(),
                                        role = UserRole.Regular)
    
    def test_register(self):        
        #1. Arrange        
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available,
                    owner = self.user)
        
        #2. Act
        self.tool_service.register(tool)
        
        #3. Assert
        self.assertEqual('test name', Tool.objects.get(name = 'test name').name, 'Did not insert the tool')
        
    def test_update(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available,
                    owner = self.user)
        
        tool.save()
        
        tool = Tool.objects.get(name = 'test name')
        
        tool.description = 'test description modified'
        
        #2. Act
        self.tool_service.update(tool, self.user.id)
        
        #3. Assert
        self.assertEqual('test description modified', Tool.objects.get(name = 'test name').description, 'Did not update the tool')
        
    def test_deregister(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available,
                    owner = self.user)
        
        tool.save()
        
        tool = Tool.objects.get(name = 'test name')
        
        #2. Act
        self.tool_service.deregister(tool.id)
        
        #3. Assert
        self.assertEqual(False, Tool.objects.get(name = 'test name').active, 'Did not deactivate the tool')
        
    def test_withhold(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available,
                    owner = self.user)
        
        tool.save()
        
        tool = Tool.objects.get(name = 'test name')
        
        #2. Act
        self.tool_service.withhold(tool.id)
        
        #3. Assert
        self.assertEqual(ToolStatus.Unavailable, Tool.objects.get(name = 'test name').status, 'Did not withhold the tool')
    
    def test_release(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Unavailable,
                    owner = self.user)
        
        tool.save()
        
        tool = Tool.objects.get(name = 'test name')
        
        #2. Act
        self.tool_service.release(tool.id)
        
        #3. Assert
        self.assertEqual(ToolStatus.Available, Tool.objects.get(name = 'test name').status, 'Did not release the tool')

    def test_get_tools_owned_by_user(self):
        #1. Arrange
        
        other_user = User.objects.create(password = '123456',
                                         email = 'othertestuser@test.com',
                                         name = 'other test name',
                                         lastname = 'other test lastname',
                                         registration_date = datetime.now().date(),
                                         house_number = 'other test number',
                                         street_name = 'other test street',
                                         phone_number = '5859571564',
                                         last_login_date = datetime.now(),
                                         preferred_pickup_location = 'other test pickup location',
                                         email_notifications = True,
                                         preferred_contact_method = 'other test contact method',
                                         role = UserRole.Regular)
        
        tool1 = Tool(name = 'test name 1',
                     description = 'test description 1',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool2 = Tool(name = 'test name 2',
                     description = 'test description 2',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool3 = Tool(name = 'test name 3',
                     description = 'test description 3',
                     active = False,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool4 = Tool(name = 'test name 4',
                     description = 'test description 4',
                     active = True,
                     status = ToolStatus.Available,
                     owner = other_user)  
        
        tool1.save()
        tool2.save()
        tool3.save()
        tool4.save()
        
        #2. Act
        tools = self.tool_service.get_tools_owned_by_user(self.user.id)
        
        #3. Assert
        self.assertEqual(2, tools.count(), 'Did not retrieve all the tools owned by the user')

    def test_get_all_tools(self):
        #1. Arrange
        tool1 = Tool(name = 'test name 1',
                     description = 'test description 1',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool2 = Tool(name = 'test name 2',
                     description = 'test description 2',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool3 = Tool(name = 'test name 3',
                     description = 'test description 3',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)        
        
        tool1.save()
        tool2.save()
        tool3.save()
        
        #2. Act
        tools = self.tool_service.get_all_tools()
        
        #3. Assert
        self.assertEqual(3, tools.count(), 'Did not retrieve all the tools')
        
    def test_get_tools_in_zipcode(self):
        #1. Arrange        
        near_user = User.objects.create(email = 'near@near.com',
                                        zip_code = '11111',
                                        role = UserRole.Regular,
                                        registration_date = datetime.now().date(),
                                        last_login_date = datetime.now())
        
        far_user = User.objects.create(email = 'far@far.com',
                                       zip_code = '22222',
                                       role = UserRole.Regular,
                                       registration_date = datetime.now().date(),
                                       last_login_date = datetime.now())
        
        near_tool1 = Tool(name = 'near tool 1',
                          description = 'near description',
                          active = True,
                          status = ToolStatus.Available,
                          owner = near_user)
        
        near_tool2 = Tool(name = 'near tool 2',
                          description = 'near description',
                          active = True,
                          status = ToolStatus.Available,
                          owner = near_user)
        
        far_tool = Tool(name = 'far tool',
                        description = 'far description',
                        active = True,
                        status = ToolStatus.Available,
                        owner = far_user)

        near_tool1.save()
        near_tool2.save()
        far_tool.save()
        
        #2. Act
        tools = self.tool_service.get_tools('', self.user.id)
        
        #3. Assert
        self.assertEqual(2, tools.count(), 'Did not retrieve the tools in the zip code')

    def test_get_tools_exclude_unavailable(self):
        #1. Arrange        
        tool1 = Tool(name = 'near tool 1',
                     description = 'near description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool2 = Tool(name = 'near tool 2',
                     description = 'near description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        unavailable_tool = Tool(name = 'far tool',
                                description = 'far description',
                                active = True,
                                status = ToolStatus.Unavailable,
                                owner = self.user)

        tool1.save()
        tool2.save()
        unavailable_tool.save()
        
        #2. Act
        tools = self.tool_service.get_tools('', self.user.id)
        
        #3. Assert
        self.assertEqual(2, tools.count(), 'Did not exclude unavailable tools')
    
    def test_get_tools_exclude_not_active(self):
        #1. Arrange        
        tool1 = Tool(name = 'near tool 1',
                     description = 'near description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool2 = Tool(name = 'near tool 2',
                     description = 'near description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        not_active_tool = Tool(name = 'far tool',
                               description = 'far description',
                               active = False,
                               status = ToolStatus.Unavailable,
                               owner = self.user)

        tool1.save()
        tool2.save()
        not_active_tool.save()
        
        #2. Act
        tools = self.tool_service.get_tools('', self.user.id)
        
        #3. Assert
        self.assertEqual(2, tools.count(), 'Did not exclude not active tools')
        
    def test_get_tools_with_search(self):
        #1. Arrange        
        tool1 = Tool(name = 'tool name foo',
                     description = 'tool description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)
        
        tool2 = Tool(name = 'tool name',
                     description = 'tool description bar',
                     active = True,
                     status = ToolStatus.Available,
                     owner = self.user)

        tool1.save()
        tool2.save()
        
        #2. Act
        tools = self.tool_service.get_tools('foo', self.user.id)
        
        #3. Assert
        self.assertEqual(1, tools.count(), 'Did not search with supplied term')
        
    def test_get_tools_with_all_conditions(self):
        #1. Arrange
        near_user = User.objects.create(email = 'near@near.com',
                                        zip_code = '11111',
                                        role = UserRole.Regular,
                                        registration_date = datetime.now().date(),
                                        last_login_date = datetime.now())
        
        far_user = User.objects.create(email = 'far@far.com',
                                       zip_code = '22222',
                                       role = UserRole.Regular,
                                       registration_date = datetime.now().date(),
                                       last_login_date = datetime.now())
        
        tool_match = Tool(name = 'tool name foo',
                     description = 'tool description',
                     active = True,
                     status = ToolStatus.Available,
                     owner = near_user)
        
        tool_not_match_search = Tool(name = 'tool name',
                                     description = 'tool description',
                                     active = True,
                                     status = ToolStatus.Available,
                                     owner = near_user)
        
        tool_not_match_zip_code = Tool(name = 'tool name foo',
                                       description = 'tool description',
                                       active = True,
                                       status = ToolStatus.Available,
                                       owner = far_user)
        
        tool_not_match_not_active = Tool(name = 'tool name foo',
                                         description = 'tool description',
                                         active = False,
                                         status = ToolStatus.Available,
                                         owner = near_user)
        
        tool_not_match_unavailable = Tool(name = 'tool name foo',
                                          description = 'tool description bar',
                                          active = True,
                                          status = ToolStatus.Unavailable,
                                          owner = near_user)

        tool_match.save()
        tool_not_match_search.save()
        tool_not_match_zip_code.save()
        tool_not_match_not_active.save()
        tool_not_match_unavailable.save()
        
        #2. Act
        tools = self.tool_service.get_tools('foo', self.user.id)
        
        #3. Assert
        self.assertEqual(1, tools.count(), 'Did not apply all search conditions')
    
    def test_get_tool(self):
        #1. Arrange
        tool = Tool(name = 'test name',
                    description = 'test description',
                    active = True,
                    status = ToolStatus.Available,
                    owner = self.user)
        
        tool.save()
        
        tool = Tool.objects.get(name = 'test name')
        
        #2. Act
        tool = self.tool_service.get_tool(tool.id)
        
        #3. Assert
        self.assertEqual('test name', tool.name, 'Did not retrieve the tool')

    
    
    
