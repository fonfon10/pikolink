class HomeController < ApplicationController

def index

end


def select
	@thisengineer = Engineer.find(params[:id])
  thisengineer = @thisengineer.id

end



def create
  if params[:long_link] 
    @link = params[:long_link]

		@thisengineer = Engineer.find(params[:engineer])

    puts ("Current User:"+current_user.email.to_s)
    puts ("engineer:"+@thisengineer.firstname.to_s)

    @short_link = Shortener::ShortenedUrl.generate(@link, owner: @thisengineer, fresh: true)
    redirect_to home_path(@short_link.id)
  end 
end


def show
  @short_link = Shortener::ShortenedUrl.find(params[:id])    
end


end
