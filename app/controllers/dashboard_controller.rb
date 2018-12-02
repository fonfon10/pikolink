class DashboardController < ApplicationController

  before_action :authenticate_user!


  def show
#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)


	#user = User.find(current_user)
	@engineers = current_user.engineers

	links = []

	@engineers.each do |engineer|

		link = engineer.shortened_urls
		links = links + link

	end

	@links = links





#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)

 


 #   @engineers = Engineer.all



 # @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
 # @engineers = @q.result.includes(:company).page(params[:page])





  end
end




      