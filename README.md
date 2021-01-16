# Service_Control_Policies_for_non_AWS_Organization_Accounts
Sometimes you have users within your AWS account that go beyond their limits and try to change AWS policies and roles, this python program fix that issue. The python must be executed every certain period in order to always ensure the correct policies are in place.

For example if a user delete a policy within an specified role, group or user, because someway he had the authority to do this action and you as the administrator knows that this policy must remain at all times, this program could save you a lot of time. You must be aware that if you enable cloudtrail previously, additional fees could apply depending on the period that you set to run the program.
