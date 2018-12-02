class DashboardController < ApplicationController

  before_action :authenticate_user!


  def show


	#user = User.find(current_user)
	@engineers = current_user.engineers

	engineers_id = []

	@engineers.each do |engineer|

		engineers_id << engineer.id

	end


    @q = Shortener::ShortenedUrl.where("owner_id IN (?)",engineers_id).ransack(params[:q])
    @shortened_urls = @q.result.includes(:owner).order(:owner_id).page params[:page]


  

    #.includes(:unique_key).order(:owner_id).page params[:page]





#  @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
#  @engineers = @q.result.includes(:company).page(params[:page])




#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)



#	links = []

#	@engineers.each do |engineer|

#		link = engineer.shortened_urls
#		links = links + link

#	end

#	@links = links.order(:updated_at).page params[:page]





#    @links = Shortener::ShortenedUrl.where("owner_id = ?",current_user).paginate(:page => params[:page], :per_page => 15)

 


 #   @engineers = Engineer.all



 # @q = Engineer.where(user_id: current_user.id).ransack(params[:q])
 # @engineers = @q.result.includes(:company).page(params[:page])





  end
end




      