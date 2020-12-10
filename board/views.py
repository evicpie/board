from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from .models import Board

class BoardListView(ListView):
    model = Board
    paginate_by = 10

def board_grid(request):
    boards = Board.objects.filter(status = "normal")
    print('boards:', boards)
    paginator = Paginator(boards, 5) # 게시물 5개 제한
    page = request.GET.get('page')  # ?page=1

    boards = paginator.get_page(page)

    return render(request,'board/board_grid.html', {'boards':boards})

class BoardCreateView(CreateView):
    model = Board
    fields = ['title', 'content', 'photo']
    template_name_suffix = '_create'

    def form_valid(self, form):
        form.instance.author_id = self.request.user.id
        if form.is_valid():
            form.instance.save()
            return redirect('/')
        else:
            return self.render_to_response({'form':form})

class BoardDetailView(DetailView):
    model = Board

class BoardUpdateView(UpdateView):
    model = Board
    fields = ['title', 'content', 'photo']
    template_name_suffix = '_update'

class BoardDeleteView(DeleteView):
    model = Board
    success_url = reverse_lazy('board:list')
