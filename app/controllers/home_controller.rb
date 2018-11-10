class HomeController < ApplicationController

def index

end


def select
end



def create
  if params[:long_link] 
    @link = params[:long_link]
    @short_link = Shortener::ShortenedUrl.generate(@link)
    redirect_to home_path(@short_link.id)
  end 
end


def show
  @short_link = Shortener::ShortenedUrl.find(params[:id])    
end


end
