class HomeController < ApplicationController

def index

end


def select
	@thisowner = Owner.find(params[:id])
  thisowner = @thisowner.id

end



def create
  if params[:long_link] 
    @link = params[:long_link]
    @category = params[:category]

		@thisowner = Owner.find(params[:owner])

    puts ("Current User:"+current_user.email.to_s)
    puts ("engineer:"+@thisowner.firstname.to_s)

    @short_link = Shortener::ShortenedUrl.generate(@link, owner: @thisowner, fresh: true, category: @category)
    redirect_to home_path(@short_link.id)
  end 
end


def show
  @short_link = Shortener::ShortenedUrl.find(params[:id])    
end


end
