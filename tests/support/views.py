from armstrong.core.arm_sections.views import SimpleSectionView

from .models import CustomSection


class CustomSectionView(SimpleSectionView):
    def get(self, request, **kwargs):
        self.object = self.get_object(queryset=CustomSection.objects.all())
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)
